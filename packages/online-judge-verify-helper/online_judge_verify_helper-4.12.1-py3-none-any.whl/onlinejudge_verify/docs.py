# -*- coding: utf-8 -*-
import glob
import hashlib
import os
import pathlib
import re
import shutil
import traceback
# typing.OrderedDict is not recognized by mypy
from collections import OrderedDict
from enum import Enum
from logging import getLogger
from typing import IO, Any, Dict, List

import onlinejudge_verify.languages
import pkg_resources
import yaml
from onlinejudge_verify.marker import get_verification_marker
from onlinejudge_verify.utils import is_verification_file

logger = getLogger(__name__)

package = 'onlinejudge_verify_resources'
assets_site_header_txt = pkg_resources.resource_string(package, 'assets/site-header.txt')
deployed_assets = [
    {
        'path': pathlib.Path('assets/css/copy-button.css'),
        'data': pkg_resources.resource_string(package, 'assets/css/copy-button.css'),
    },
    {
        'path': pathlib.Path('assets/js/copy-button.js'),
        'data': pkg_resources.resource_string(package, 'assets/js/copy-button.js'),
    },
    {
        'path': pathlib.Path('Gemfile'),
        'data': pkg_resources.resource_string(package, 'Gemfile'),
    },
]


class FileParser:
    # ファイルパスをもらって、行ごとに分ける
    def __init__(self, file_path: pathlib.Path) -> None:
        if not file_path.exists():
            raise FileNotFoundError('{} does not exist'.format(file_path))
        with open(file_path, 'rb') as f:
            self.lines = [line.decode().strip() for line in f.readlines()]

    # タグをもらって、コンテンツの配列を出す
    def get_contents_by_tag(self, tag_name: str, *, l_pat: str = '', r_pat: str = '', re_escape: bool = True) -> List[str]:
        if re_escape:
            tag_name = re.escape(tag_name)
        l_pat, r_pat = re.escape(l_pat), re.escape(r_pat)

        reg1, reg2 = r'^.*' + tag_name, r'^.*' + tag_name
        if l_pat != '':
            reg1 += r'.*' + l_pat
            reg2 += r'.*' + l_pat
        reg1 += r'.*'
        reg2 += r'(.*)'
        if r_pat != '':
            reg1 += r_pat + r'.*'
            reg2 += r_pat + r'.*'
        reg1 += r'$'
        reg2 += r'$'

        matches = [line for line in self.lines if re.match(reg1, line)]
        results = [re.sub(reg2, r'\1', line).strip() for line in matches]
        return results


class VerificationStatus(Enum):
    VERIFIED = ':heavy_check_mark:'
    QUESTION = ':question:'
    FAILED = ':x:'
    DEFAULT = ':warning:'


# 現状は C++ のみのサポートを考える
class CppFile:
    file_path: pathlib.Path  # 対象としている C++ ファイル (source_path 内にあるファイル) への絶対パス
    source_path: pathlib.Path  #  検索対象となっているディレクトリへの絶対パス
    parser: FileParser
    brief: List[str]  # @brief で指定された文字列
    see: List[str]  # @see で指定された文字列
    docs: List[pathlib.Path]  # @docs で指定されたファイルへの絶対パス
    depends: List[pathlib.Path]  # @depends で指定されたファイルへの絶対パス
    required: List[pathlib.Path]
    verification_status: VerificationStatus

    def __init__(self, file_path: pathlib.Path, source_path: pathlib.Path) -> None:
        self.file_path = file_path.resolve()
        self.source_path = source_path.resolve()
        self.parser = FileParser(file_path)
        self.required = []

        self.brief = self.parser.get_contents_by_tag(r'@brief')

        # file 指定が空なら、source_path から見た file_path へのパスをタイトルにする
        title_list = self.parser.get_contents_by_tag(r'@title')
        if title_list == []:
            if len(self.brief) > 0:
                self.title = self.brief[0] + ' <small>(' + str(self.file_path.relative_to(self.source_path)) + ')</small>'
                self.brief = self.brief[1:]
            else:
                self.title = str(self.file_path.relative_to(self.source_path))
        else:
            # @title が複数あるなら最後を採用？？
            self.title = title_list[-1]
        self.title = self.title.replace('[', '\[').replace(']', '\]')

        # category 指定が空なら、source_path から見た file_path が属するディレクトリ名をカテゴリにする
        category_list = self.parser.get_contents_by_tag(r'@category')
        if category_list == []:
            self.category = str(self.file_path.parent.relative_to(self.source_path))
        else:
            self.category = category_list[-1]

        # pathlib 型に直し、相対パスである場合は絶対パスに直す
        docs_list = self.parser.get_contents_by_tag(r'@docs')
        self.docs = [pathlib.Path(path) for path in docs_list]
        self.docs = self.to_abspath(self.docs)

        # see で指定されるのは URL: パス修正は不要
        self.see = self.parser.get_contents_by_tag(r'(?:@see|@sa)', re_escape=False)

        # language object を用意しておく
        language = onlinejudge_verify.languages.get(self.file_path)
        assert language is not None

        # language.list_dependencie() をもとに sself.depends を絶対パスの list として持つ
        try:
            self.depends = language.list_dependencies(self.file_path, basedir=pathlib.Path.cwd())
        except:
            # 失敗したら中断
            traceback.print_exc()
            self.depends = []
            self.verification_status = VerificationStatus.FAILED
            return
        self.depends.extend(map(pathlib.Path, self.parser.get_contents_by_tag(r'@depends')))
        self.depends = sorted(set(self.to_abspath(self.depends)))

        # language.list_attributes() をもとに PROBLEM のデータを取得
        try:
            attributes = language.list_attributes(self.file_path, basedir=pathlib.Path.cwd())
        except:
            # 失敗したら中断
            traceback.print_exc()
            self.verification_status = VerificationStatus.FAILED
            return
        if 'PROBLEM' in attributes:
            self.see.append(attributes['PROBLEM'])

        # 表示するverification statusを決める
        is_verified = get_verification_marker().is_verified(self.file_path.relative_to(self.source_path))
        is_failed = get_verification_marker().is_failed(self.file_path.relative_to(self.source_path))
        if is_verified:
            self.verification_status = VerificationStatus.VERIFIED
        elif is_failed:
            self.verification_status = VerificationStatus.FAILED
        else:
            self.verification_status = VerificationStatus.DEFAULT

    # self.file_path からの相対パスを絶対パスに直す
    def to_abspath(self, item_list: List[pathlib.Path]) -> List[pathlib.Path]:
        result, file_dir = [], self.file_path.parent
        for item in item_list:
            abspath_cand = file_dir / item
            # とりあえず連結して存在するなら相対パス扱い
            if abspath_cand.exists():
                abspath_cand = abspath_cand.resolve()
                if abspath_cand != self.file_path:
                    result.append(abspath_cand)
            # 絶対パス扱いにしたものを読んで存在しないなら捨てる
            elif item.exists():
                item = item.resolve()
                if item != self.file_path:
                    result.append(item)
        return result


class MarkdownPage:
    cpp_source_path: pathlib.Path
    md_destination_path: pathlib.Path
    destination: pathlib.Path

    def __init__(self) -> None:
        self.cpp_source_path = pathlib.Path()
        self.md_destination_path = pathlib.Path()
        self.destination = pathlib.Path()

    # file_path の markdown 生成先はどのような絶対パスになるべきか
    # prefix は [cpp_source_path までのパス] でなければならない
    # [markdown 生成先ディレクトリまでのパス] + [file_type] + [cpp_source_path より深いパス] を返す？
    def get_destination(self, file_path: pathlib.Path, file_type: str) -> pathlib.Path:
        try:
            file_path.relative_to(self.cpp_source_path)
        except ValueError:
            raise ValueError('{} does not have prefix {}\n'.format(str(file_path), str(self.cpp_source_path)))

        file_path = file_path.resolve()
        path_suf = file_path.relative_to(self.cpp_source_path)
        return (self.md_destination_path / file_type / path_suf).resolve()

    # ページ A からページ B (link_href) への相対パスを得る
    # 全部絶対パスで持っているので relpath するだけでいいはず
    def get_link(self, link_href: pathlib.Path) -> str:
        return os.path.relpath(str(link_href), str(self.destination.parent))

    def get_linktag(self, text: str, link: str) -> str:
        link_text = link.replace('"', '\"')
        return r'<a href="{}">{}</a>'.format(link_text, text)

    def make_directory(self) -> None:
        dir_name = self.destination.parent
        dir_name.mkdir(parents=True, exist_ok=True)

    def include_js(self, file_object: IO, js_file_name: pathlib.Path) -> None:
        js_file_link = self.get_link(js_file_name)
        html = '<script type="text/javascript" src="{}"></script>\n'.format(js_file_link)
        file_object.write(html.encode())

    def include_css(self, file_object: IO, css_file_name: pathlib.Path) -> None:
        css_file_link = self.get_link(css_file_name)
        html = '<link rel="stylesheet" href="{}" />\n'.format(css_file_link)
        file_object.write(html.encode())


class MarkdownArticle(MarkdownPage):
    file_class: CppFile
    cpp_source_path: pathlib.Path
    md_destination_path: pathlib.Path
    destination: pathlib.Path
    mark: VerificationStatus

    def __init__(self, file_class: CppFile, file_type: str, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path) -> None:
        self.file_class = file_class
        self.cpp_source_path = cpp_source_path.resolve()
        self.md_destination_path = md_destination_path.resolve()
        self.destination = self.get_destination(self.file_class.file_path, file_type)
        self.mark = self.file_class.verification_status

    # include (mathjax, js, css)
    def write_header(self, file_object: IO) -> None:
        file_object.write(b'---\nlayout: default\n---\n\n')
        file_object.write(assets_site_header_txt)
        self.include_js(file_object, self.md_destination_path / './assets/js/copy-button.js')
        self.include_css(file_object, self.md_destination_path / './assets/css/copy-button.css')
        file_object.write(b'\n\n')

    def write_title(self, file_object: IO, category: str) -> None:
        file_object.write('# {} {}\n\n'.format(self.mark.value, self.file_class.title).encode())

        # back to top
        back_to_top_link = self.get_link(self.md_destination_path / 'index.html')
        file_object.write('{}\n\n'.format(self.get_linktag('Back to top page', back_to_top_link)).encode())

        top_page_category_link = back_to_top_link + '#' + hashlib.md5(category.encode()).hexdigest()
        file_object.write('* category: {}\n'.format(self.get_linktag(category, top_page_category_link)).encode())
        github_link = '{{ site.github.repository_url }}' + '/blob/{}/{}'.format('master', str(self.file_class.file_path.relative_to(self.file_class.source_path)))
        file_object.write('* {}\n    - Last commit date: {}\n'.format(self.get_linktag('View this file on GitHub', github_link), get_verification_marker().get_current_timestamp(self.file_class.file_path)).encode())
        file_object.write(b'\n\n')

    def write_contents(self, file_object: IO, path_to_title: 'OrderedDict[pathlib.Path, str]', path_to_verification: Dict[pathlib.Path, VerificationStatus]) -> None:
        back_to_top_link = self.get_link(self.md_destination_path / 'index.html')

        # see, docs (絶対パス)
        for see in self.file_class.see:
            file_object.write('* see: {}\n'.format(self.get_linktag(see, see)).encode())
        for docs in self.file_class.docs:
            file_object.write(b'\n\n')
            with open(docs, 'rb') as f:
                file_object.write(f.read())
        file_object.write(b'\n\n')

        # cpp (絶対パス) => (cpp|test.cpp) (絶対パス): リンクは相対パスに
        self.file_class.depends = sorted(list(set(self.file_class.depends)))
        if self.file_class.depends != []:
            file_object.write(b'## Depends on\n\n')
            for depends in self.file_class.depends:
                if depends not in path_to_verification:
                    raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(depends))
                mark = path_to_verification[depends]

                if depends not in path_to_title:
                    raise FileNotFoundError('{} seems not to exist in path_to_title'.format(depends))
                title = path_to_title[depends]

                file_type = 'verify' if is_verification_file(depends) else 'library'
                link = self.get_link(self.get_destination(depends, file_type)) + '.html'
                file_object.write('* {} {}\n'.format(mark.value, self.get_linktag(title, link)).encode())
            file_object.write(b'\n\n')

        required_file_list = [f for f in self.file_class.required if not is_verification_file(f)]
        verified_file_list = [f for f in self.file_class.required if is_verification_file(f)]

        # ビルド対象ファイルが test.cpp の場合、それに依存している test.cpp ファイルは Verified ではなく Required に入れる
        if is_verification_file(self.file_class.file_path):
            required_file_list.extend(verified_file_list)
            verified_file_list = []

        required_file_list = sorted(set(required_file_list))
        verified_file_list = sorted(set(verified_file_list))

        # cpp <= cpp または test.cpp <= test.cpp
        if required_file_list != []:
            file_object.write(b'## Required by\n\n')
            for required in required_file_list:
                if required not in path_to_verification:
                    raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(required))
                mark = path_to_verification[required]

                if required not in path_to_title:
                    raise FileNotFoundError('{} seems not to exist in path_to_title'.format(required))
                title = path_to_title[required]

                file_type = 'verify' if is_verification_file(required) else 'library'
                link = self.get_link(self.get_destination(required, file_type)) + '.html'
                file_object.write('* {} {}\n'.format(mark.value, self.get_linktag(title, link)).encode())
            file_object.write(b'\n\n')

        # cpp => test.cpp
        if verified_file_list != []:
            file_object.write(b'## Verified with\n\n')
            for verified in verified_file_list:
                if verified not in path_to_verification:
                    raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(verified))
                mark = path_to_verification[verified]

                if verified not in path_to_title:
                    raise FileNotFoundError('{} seems not to exist in path_to_title'.format(verified))
                title = path_to_title[verified]

                link = self.get_link(self.get_destination(verified, 'verify')) + '.html'
                file_object.write('* {} {}\n'.format(mark.value, self.get_linktag(title, link)).encode())
            file_object.write(b'\n\n')

        # source code
        file_object.write(b'## Code\n\n')
        file_object.write(b'<a id="unbundled"></a>\n')
        file_object.write(b'{% raw %}\n```cpp\n')
        with open(self.file_class.file_path, 'rb') as f:
            file_object.write(f.read())
        file_object.write(b'\n```\n{% endraw %}\n\n')

        language = onlinejudge_verify.languages.get(self.file_class.file_path)
        assert language is not None
        try:
            bundled_code = language.bundle(self.file_class.file_path, basedir=pathlib.Path.cwd())
        except Exception:
            logger.warning("failed to bundle: %s", str(self.file_class.file_path))
            bundled_code = traceback.format_exc().encode()
        file_object.write(b'<a id="bundled"></a>\n')
        file_object.write(b'{% raw %}\n```cpp\n')
        file_object.write(bundled_code)
        file_object.write(b'\n```\n{% endraw %}\n\n')

        # back to top
        file_object.write('{}\n\n'.format(self.get_linktag('Back to top page', back_to_top_link)).encode())

    def build(self, path_to_title: 'OrderedDict[pathlib.Path, str]', path_to_verification: Dict[pathlib.Path, VerificationStatus], category: str) -> None:
        self.make_directory()
        with open(str(self.destination) + '.md', mode='wb') as file_object:
            self.write_header(file_object)
            self.write_title(file_object, category)
            self.write_contents(file_object, path_to_title, path_to_verification)


class MarkdownTopPage(MarkdownPage):
    cpp_source_path: pathlib.Path
    md_destination_path: pathlib.Path
    destination: pathlib.Path
    config: Dict[str, Any]

    def __init__(self, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path, config: Dict[str, Any]) -> None:
        self.cpp_source_path = cpp_source_path.resolve()
        self.md_destination_path = md_destination_path.resolve()
        self.destination = md_destination_path / 'index'
        self.config = config

    def write_header(self, file_object: IO) -> None:
        file_object.write(b'---\nlayout: default\n---\n\n')
        file_object.write(assets_site_header_txt)
        self.include_js(file_object, self.md_destination_path / './assets/js/copy-button.js')
        self.include_css(file_object, self.md_destination_path / './assets/css/copy-button.css')
        file_object.write(b'\n\n')

    def write_title(self, file_object: IO) -> None:
        # GitHub Pages が設定してくれる site.title や site.description を使う
        # see: http://jekyll.github.io/github-metadata/
        file_object.write(b'# {{ site.title }}\n\n')
        file_object.write(b'[![Actions Status]({{ site.github.repository_url }}/workflows/verify/badge.svg)]({{ site.github.repository_url }}/actions)\n')
        file_object.write(b'<a href="{{ site.github.repository_url }}"><img src="https://img.shields.io/github/last-commit/{{ site.github.owner_name }}/{{ site.github.repository_name }}" /></a>\n\n')
        file_object.write(b"""{% if site.github.project_tagline %}{{ site.github.project_tagline }}{% else %}This documentation is automatically generated by <a href="https://github.com/online-judge-tools/verification-helper">online-judge-tools/verification-helper</a>.{% endif %}\n\n""")

    def write_contents(
            self,
            file_object: IO,
            verify_files: 'OrderedDict[pathlib.Path, CppFile]',
            library_files: 'OrderedDict[pathlib.Path, CppFile]',
            library_category_to_path: 'OrderedDict[str, List[pathlib.Path]]',
            path_to_title: 'OrderedDict[pathlib.Path, str]',
            path_to_verification: Dict[pathlib.Path, VerificationStatus],
    ) -> None:
        if library_files != {}:
            file_object.write(b'## Library Files\n\n')
            for category, library_list in library_category_to_path.items():
                file_object.write('<div id="{}"></div>\n\n'.format(hashlib.md5(category.encode()).hexdigest()).encode())
                file_object.write('### {}\n\n'.format(category).encode())
                for library_file in library_list:
                    if library_file not in path_to_verification:
                        raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(library_file))
                    mark = path_to_verification[library_file]

                    if library_file not in path_to_title:
                        raise FileNotFoundError('{} seems not to exist in path_to_title'.format(library_file))
                    title = path_to_title[library_file]

                    link = self.get_link(self.get_destination(library_file, 'library')) + '.html'
                    file_object.write('* {} {}\n'.format(mark.value, self.get_linktag(title, link)).encode())
                file_object.write(b'\n\n')

        if verify_files != {}:
            file_object.write(b'## Verify Files\n\n')
            for verify_file in verify_files.keys():
                if verify_file not in path_to_verification:
                    raise FileNotFoundError('{} seems not to exist in path_to_verification'.format(verify_file))
                mark = path_to_verification[verify_file]

                if verify_file not in path_to_title:
                    raise FileNotFoundError('{} seems not to exist in path_to_title'.format(verify_file))
                title = path_to_title[verify_file]

                link = self.get_link(self.get_destination(verify_file, 'verify')) + '.html'
                file_object.write('* {} {}\n'.format(mark.value, self.get_linktag(title, link)).encode())
            file_object.write(b'\n\n')

    def build(
            self,
            verify_files: 'OrderedDict[pathlib.Path, CppFile]',
            library_files: 'OrderedDict[pathlib.Path, CppFile]',
            library_category_to_path: 'OrderedDict[str, List[pathlib.Path]]',
            path_to_title: 'OrderedDict[pathlib.Path, str]',
            path_to_verification: Dict[pathlib.Path, VerificationStatus],
    ) -> None:
        self.make_directory()
        with open(str(self.destination) + '.md', mode='wb') as file_object:
            self.write_header(file_object)
            self.write_title(file_object)
            self.write_contents(
                file_object,
                verify_files,
                library_files,
                library_category_to_path,
                path_to_title,
                path_to_verification,
            )


class PagesBuilder:
    def __init__(self, *, cpp_source_pathstr: str, md_destination_pathstr: str = '.verify-helper/markdown', config: Dict[str, Any] = {}) -> None:
        cpp_source_path = pathlib.Path(cpp_source_pathstr).resolve()
        md_destination_path = pathlib.Path(md_destination_pathstr).resolve()

        # (指定がなければ) config にデフォルト値を入れる
        # _config.yml を書き出す
        self.config = config
        self.build_config(md_destination_path)

        # ビルド対象ファイル一覧
        self.verify_files = self.get_files(cpp_source_path, is_verify=True)
        self.library_files = self.get_files(cpp_source_path, ignored_files=self.verify_files)

        # ファイルまでの絶対パス <-> タイトル
        self.title_to_path = self.get_title_to_path()
        self.path_to_title = self.get_path_to_title()

        # カテゴリ -> ファイルまでの絶対パスのリスト
        self.verify_category_to_path = self.get_verify_category_to_path()
        self.library_category_to_path = self.get_library_category_to_path()

        # 設定項目
        self.config = config

        # 依存関係を調べる
        self.analyze_required()

        # 各ファイルについて depends, required の対象であって @ignore されているファイルの除外
        self.remove_ignored_file_relation()

        # ファイルまでの絶対パス -> Verification Status
        self.path_to_verification = self.get_path_to_verification()

        # ページをビルド
        self.build_verify_files(cpp_source_path, md_destination_path)
        self.build_library_files(cpp_source_path, md_destination_path)
        self.build_top_page(cpp_source_path, md_destination_path)
        self.build_assets(md_destination_path)
        self.build_static_files(md_destination_path)

    def build_config(self, md_destination_path: pathlib.Path) -> None:
        # デフォルト値
        self.config.setdefault('theme', 'jekyll-theme-minimal')
        self.config.setdefault('description', '<small>This documentation is automatically generated by <a href="https://github.com/online-judge-tools/verification-helper">online-judge-tools/verification-helper</a></small>')
        self.config.setdefault('plugins', [])
        if 'jemoji' not in self.config['plugins']:
            self.config['plugins'].append('jemoji')

        dst_path = md_destination_path / '_config.yml'
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dst_path, "wb") as f:
            f.write(yaml.dump(self.config, default_flow_style=False).encode())

    # ignore されるべきなら True
    def is_ignored(self, file_path: pathlib.Path) -> bool:
        # ファイルパスに `.verify-helper` が含まれるなら除外
        if re.match(r'^.*\.verify-helper.*$', str(file_path)):
            return True

        parser = FileParser(file_path)
        ignore = []
        ignore.extend(parser.get_contents_by_tag(r'@ignore'))
        return bool(ignore)

    # source_path 内にあって拡張子末尾が extension であるファイル一覧
    # ignored_files に含まれるならば無視
    def get_files(self, source_path: pathlib.Path, *, is_verify: bool = False, ignored_files: 'OrderedDict[pathlib.Path, CppFile]' = OrderedDict()) -> 'OrderedDict[pathlib.Path, CppFile]':
        files = {}
        for path in source_path.glob(r'**/*'):
            if onlinejudge_verify.languages.get(path):
                if is_verify and not is_verification_file(path):
                    continue
                if any([path.samefile(ignored_file) for ignored_file in ignored_files]):
                    continue
                if not self.is_ignored(path):
                    path = path.resolve()
                    files[path] = CppFile(path, source_path)
        return OrderedDict(sorted(files.items(), key=lambda x: x[0]))

    # title の重複があったらナンバリング付与
    def get_title_to_path(self) -> 'OrderedDict[str, pathlib.Path]':
        title_cnt, title_num, result = {}, {}, {}  # type: Dict[str, int], Dict[str, int], Dict[str, pathlib.Path]
        for cpp_class in self.library_files.values():
            title_cnt.setdefault(cpp_class.title, 0)
            title_cnt[cpp_class.title] += 1
        for cpp_class in self.verify_files.values():
            title_cnt.setdefault(cpp_class.title, 0)
            title_cnt[cpp_class.title] += 1

        for cpp_class in self.library_files.values():
            title = cpp_class.title
            if title_cnt[title] >= 2:
                title_num.setdefault(title, 0)
                title_num[title] += 1
                title += ' ({:02})'.format(title_num[title])
            result[title] = cpp_class.file_path
            cpp_class.title = title
        for cpp_class in self.verify_files.values():
            title = cpp_class.title
            if title_cnt[title] >= 2:
                title_num.setdefault(title, 0)
                title_num[title] += 1
                title += ' ({:02})'.format(title_num[title])
            result[title] = cpp_class.file_path
            cpp_class.title = title
        return OrderedDict(sorted(result.items(), key=lambda x: x[0]))

    def get_path_to_title(self) -> 'OrderedDict[pathlib.Path, str]':
        result = {}
        for cpp_class in self.library_files.values():
            result[cpp_class.file_path] = cpp_class.title
        for cpp_class in self.verify_files.values():
            result[cpp_class.file_path] = cpp_class.title
        result = OrderedDict(sorted(result.items(), key=lambda x: x[0]))

        # verify_files, library_files のタイトルを振り直す
        for verify in self.verify_files.keys():
            self.verify_files[verify].title = result[verify]
        for library in self.library_files.keys():
            self.library_files[library].title = result[library]

        return result

    def get_verify_category_to_path(self) -> 'OrderedDict[str, List[pathlib.Path]]':
        verify_result = {}  # type: Dict[str, List[pathlib.Path]]
        for cpp_class in self.verify_files.values():
            verify_result.setdefault(cpp_class.category, [])
            verify_result[cpp_class.category].append(cpp_class.file_path)
        for file_path_list in verify_result.values():
            file_path_list.sort()
        return OrderedDict(sorted(verify_result.items(), key=lambda x: x[0]))

    def get_library_category_to_path(self) -> 'OrderedDict[str, List[pathlib.Path]]':
        library_result = {}  # type: Dict[str, List[pathlib.Path]]
        for cpp_class in self.library_files.values():
            library_result.setdefault(cpp_class.category, [])
            library_result[cpp_class.category].append(cpp_class.file_path)
        for file_path_list in library_result.values():
            file_path_list.sort()
        return OrderedDict(sorted(library_result.items(), key=lambda x: x[0]))

    def analyze_required(self) -> None:
        map_required = {}  # type: Dict[pathlib.Path, List[pathlib.Path]]
        for cpp_class in self.library_files.values():
            for depends in cpp_class.depends:
                map_required.setdefault(depends, [])
                map_required[depends].append(cpp_class.file_path)
        for cpp_class in self.verify_files.values():
            for depends in cpp_class.depends:
                map_required.setdefault(depends, [])
                map_required[depends].append(cpp_class.file_path)

        for depends_list in map_required.values():
            depends_list.sort()

        for cpp_file in self.library_files.keys():
            map_required.setdefault(cpp_file, [])
            self.library_files[cpp_file].required = sorted(map_required[cpp_file])

        for cpp_file in self.verify_files.keys():
            map_required.setdefault(cpp_file, [])
            self.verify_files[cpp_file].required = sorted(map_required[cpp_file])

    # @ignore されていないファイルのみを depends, required に残す
    # 本来あるべきファイルが存在しない場合もここで怒られるはず？？
    def remove_ignored_file_relation(self) -> None:
        for cpp_file, cpp_class in self.verify_files.items():
            depends_list_verify, required_list_verify = [], []  # type: List[pathlib.Path], List[pathlib.Path]
            for depends in cpp_class.depends:
                if not self.is_ignored(depends):
                    depends_list_verify.append(depends)
            for required in cpp_class.required:
                if not self.is_ignored(required):
                    required_list_verify.append(required)
            self.verify_files[cpp_file].depends = depends_list_verify
            self.verify_files[cpp_file].required = required_list_verify

        for cpp_file, cpp_class in self.library_files.items():
            depends_list_library, required_list_library = [], []  # type: List[pathlib.Path], List[pathlib.Path]
            for depends in cpp_class.depends:
                if not self.is_ignored(depends):
                    depends_list_library.append(depends)
            for required in cpp_class.required:
                if not self.is_ignored(required):
                    required_list_library.append(required)
            self.library_files[cpp_file].depends = depends_list_library
            self.library_files[cpp_file].required = required_list_library

    def get_path_to_verification(self) -> Dict[pathlib.Path, VerificationStatus]:
        result = {}  # type: Dict[pathlib.Path, VerificationStatus]
        # .test.cpp の verify 状況確認
        for cpp_file, cpp_class in self.verify_files.items():
            result[cpp_file] = cpp_class.verification_status

        # .cpp は、それを必要としている .test.cpp が少なくとも 1 つ存在し
        # 全ての .test.cpp が verify 済みなら OK
        for cpp_file, cpp_class in self.library_files.items():
            # cpp_fileを必要としている .test.cpp のstatusのlist
            required_verification_statuses = []
            for verify in cpp_class.required:
                if is_verification_file(verify):
                    required_verification_statuses.append(result[verify])
            # verification statusを解決する
            if len(required_verification_statuses) == 0:
                # 一つも .test.cpp が見つからなかったらverifyされていない
                result[cpp_file] = VerificationStatus.DEFAULT
            elif all(status == VerificationStatus.FAILED for status in required_verification_statuses):
                # cpp_fileを必要としている全てのtestでfailedならfailedとする
                result[cpp_file] = VerificationStatus.FAILED
            elif all(status == VerificationStatus.VERIFIED for status in required_verification_statuses):
                # 上記以外でcpp_fileを必要としている .test.cpp が全てverifiedかfailedならverifiedとする
                result[cpp_file] = VerificationStatus.VERIFIED
            else:
                # 一つでもfailedならfailed、とすると自身のコードに問題ない場合も誤ってfailedとなる可能性が高まるので避けた
                result[cpp_file] = VerificationStatus.QUESTION
            self.library_files[cpp_file].verification_status = result[cpp_file]
        return result

    def build_verify_files(self, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path) -> None:
        for category, verify_path_list in self.verify_category_to_path.items():
            for matched_file_path in verify_path_list:
                verify_file_class = self.verify_files[matched_file_path]
                page = MarkdownArticle(verify_file_class, 'verify', cpp_source_path, md_destination_path)
                page.build(self.path_to_title, self.path_to_verification, category)

    def build_library_files(self, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path) -> None:
        for category, library_path_list in self.library_category_to_path.items():
            for matched_file_path in library_path_list:
                library_file_class = self.library_files[matched_file_path]
                page = MarkdownArticle(library_file_class, 'library', cpp_source_path, md_destination_path)
                page.build(self.path_to_title, self.path_to_verification, category)

    def build_top_page(self, cpp_source_path: pathlib.Path, md_destination_path: pathlib.Path) -> None:
        page = MarkdownTopPage(cpp_source_path, md_destination_path, self.config)
        page.build(
            self.verify_files,
            self.library_files,
            self.library_category_to_path,
            self.path_to_title,
            self.path_to_verification,
        )

    def build_assets(self, md_destination_path: pathlib.Path) -> None:
        assets_dir = md_destination_path / 'assets'
        if assets_dir.exists():
            shutil.rmtree(str(assets_dir))
        for asset in deployed_assets:
            path = md_destination_path / asset['path']  # type: ignore
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(path), 'wb') as fh:
                fh.write(asset['data'])  # type: ignore

    def build_static_files(self, md_destination_path: pathlib.Path) -> None:
        static_dir = pathlib.Path('.verify-helper/docs/static')
        for src_path in map(pathlib.Path, glob.glob(str(static_dir) + '/**/*', recursive=True)):
            dst_path = md_destination_path / src_path.relative_to(static_dir)
            if src_path.is_file():
                shutil.copyfile(str(src_path), str(dst_path))


def main() -> None:
    config_yml = pathlib.Path('.verify-helper/docs/_config.yml')
    if config_yml.exists():
        with open(str(config_yml)) as fh:
            config = yaml.load(fh, Loader=yaml.SafeLoader)
    else:
        config = {}  # use default settings
    config.setdefault('docs', {})

    PagesBuilder(cpp_source_pathstr='.', config=config)
