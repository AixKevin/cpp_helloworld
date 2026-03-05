#!/usr/bin/env python3
"""
LearnCpp Content Downloader
自动下载 learncpp.com.cn 的所有教程内容
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE_URL = "https://learncpp.com.cn"
OUTPUT_DIR = "."

# 章节URL映射（完整版）
CHAPTERS = {
    "chapter_0": [
        "/cpp-tutorial/introduction-to-these-tutorials/",
        "/cpp-tutorial/introduction-to-programming-languages/",
        "/cpp-tutorial/introduction-to-cplusplus/",
        "/cpp-tutorial/introduction-to-cpp-development/",
        "/cpp-tutorial/introduction-to-the-compiler-linker-and-libraries/",
        "/cpp-tutorial/installing-an-integrated-development-environment-ide/",
        "/cpp-tutorial/compiling-your-first-program/",
        "/cpp-tutorial/a-few-common-cpp-problems/",
        "/cpp-tutorial/configuring-your-compiler-build-configurations/",
        "/cpp-tutorial/configuring-your-compiler-compiler-extensions/",
        "/cpp-tutorial/configuring-your-compiler-warning-and-error-levels/",
        "/cpp-tutorial/configuring-your-compiler-choosing-a-language-standard/",
        "/cpp-tutorial/what-language-standard-is-my-compiler-using/",
    ],
    "chapter_1": [
        "/cpp-tutorial/statements-and-the-structure-of-a-program/",
        "/cpp-tutorial/comments/",
        "/cpp-tutorial/introduction-to-objects-and-variables/",
        "/cpp-tutorial/variable-assignment-and-initialization/",
        "/cpp-tutorial/introduction-to-iostream-cout-cin-and-endl/",
        "/cpp-tutorial/uninitialized-variables-and-undefined-behavior/",
        "/cpp-tutorial/keywords-and-naming-identifiers/",
        "/cpp-tutorial/whitespace-and-basic-formatting/",
        "/cpp-tutorial/introduction-to-literals-and-operators/",
        "/cpp-tutorial/introduction-to-expressions/",
        "/cpp-tutorial/developing-your-first-program/",
    ],
    "chapter_2": [
        "/cpp-tutorial/introduction-to-functions/",
        "/cpp-tutorial/function-return-values-value-returning-functions/",
        "/cpp-tutorial/void-functions-non-value-returning-functions/",
        "/cpp-tutorial/introduction-to-function-parameters-and-arguments/",
        "/cpp-tutorial/introduction-to-local-scope/",
        "/cpp-tutorial/why-functions-are-useful-and-how-to-use-them-effectively/",
        "/cpp-tutorial/forward-declarations/",
        "/cpp-tutorial/programs-with-multiple-code-files/",
        "/cpp-tutorial/naming-collisions-and-an-introduction-to-namespaces/",
        "/cpp-tutorial/introduction-to-the-preprocessor/",
        "/cpp-tutorial/header-files/",
        "/cpp-tutorial/header-guards/",
        "/cpp-tutorial/how-to-design-your-first-programs/",
    ],
    "chapter_3": [
        "/cpp-tutorial/syntax-and-semantic-errors/",
        "/cpp-tutorial/the-debugging-process/",
        "/cpp-tutorial/a-strategy-for-debugging/",
        "/cpp-tutorial/basic-debugging-tactics/",
        "/cpp-tutorial/more-debugging-tactics/",
        "/cpp-tutorial/using-an-integrated-debugger-stepping/",
        "/cpp-tutorial/using-an-integrated-debugger-running-and-breakpoints/",
        "/cpp-tutorial/using-an-integrated-debugger-watching-variables/",
        "/cpp-tutorial/using-an-integrated-debugger-the-call-stack/",
        "/cpp-tutorial/finding-issues-before-they-become-problems/",
    ],
    "chapter_4": [
        "/cpp-tutorial/introduction-to-fundamental-data-types/",
        "/cpp-tutorial/void/",
        "/cpp-tutorial/object-sizes-and-the-sizeof-operator/",
        "/cpp-tutorial/signed-integers/",
        "/cpp-tutorial/unsigned-integers-and-why-to-avoid-them/",
        "/cpp-tutorial/fixed-width-integers-and-size-t/",
        "/cpp-tutorial/introduction-to-scientific-notation/",
        "/cpp-tutorial/floating-point-numbers/",
        "/cpp-tutorial/boolean-values/",
        "/cpp-tutorial/introduction-to-if-statements/",
        "/cpp-tutorial/chars/",
        "/cpp-tutorial/introduction-to-type-conversion-and-static_cast/",
    ],
    "chapter_5": [
        "/cpp-tutorial/constant-variables-named-constants/",
        "/cpp-tutorial/literals/",
        "/cpp-tutorial/numeral-systems-decimal-binary-hexadecimal-and-octal/",
        "/cpp-tutorial/the-as-if-rule-and-compile-time-optimization/",
        "/cpp-tutorial/constant-expressions/",
        "/cpp-tutorial/constexpr-variables/",
        "/cpp-tutorial/introduction-to-stdstring/",
        "/cpp-tutorial/introduction-to-stdstring_view/",
        "/cpp-tutorial/stdstring_view-part-2/",
    ],
    "chapter_6": [
        "/cpp-tutorial/operator-precedence-and-associativity/",
        "/cpp-tutorial/arithmetic-operators/",
        "/cpp-tutorial/remainder-and-exponentiation/",
        "/cpp-tutorial/increment-decrement-operators-and-side-effects/",
        "/cpp-tutorial/the-comma-operator/",
        "/cpp-tutorial/the-conditional-operator/",
        "/cpp-tutorial/relational-operators-and-floating-point-comparisons/",
        "/cpp-tutorial/logical-operators/",
    ],
    "chapter_7": [
        "/cpp-tutorial/compound-statements-blocks/",
        "/cpp-tutorial/user-defined-namespaces-and-the-scope-resolution-operator/",
        "/cpp-tutorial/local-variables/",
        "/cpp-tutorial/introduction-to-global-variables/",
        "/cpp-tutorial/variable-shadowing-name-hiding/",
        "/cpp-tutorial/internal-linkage/",
        "/cpp-tutorial/external-linkage-and-variable-forward-declarations/",
        "/cpp-tutorial/why-non-const-global-variables-are-evil/",
        "/cpp-tutorial/inline-functions-and-variables/",
        "/cpp-tutorial/sharing-global-constants-across-multiple-files-using-inline-variables/",
        "/cpp-tutorial/static-local-variables/",
        "/cpp-tutorial/scope-duration-and-linkage-summary/",
        "/cpp-tutorial/using-declarations-and-using-directives/",
        "/cpp-tutorial/unnamed-and-inline-namespaces/",
    ],
    "chapter_8": [
        "/cpp-tutorial/control-flow-introduction/",
        "/cpp-tutorial/if-statements-and-blocks/",
        "/cpp-tutorial/common-if-statement-problems/",
        "/cpp-tutorial/constexpr-if-statements/",
        "/cpp-tutorial/switch-statement-basics/",
        "/cpp-tutorial/switch-fallthrough-and-scoping/",
        "/cpp-tutorial/goto-statements/",
        "/cpp-tutorial/introduction-to-loops-and-while-statements/",
        "/cpp-tutorial/do-while-statements/",
        "/cpp-tutorial/for-statements/",
        "/cpp-tutorial/break-and-continue/",
        "/cpp-tutorial/halts-exiting-your-program-early/",
        "/cpp-tutorial/introduction-to-random-number-generation/",
        "/cpp-tutorial/generating-random-numbers-using-mersenne-twister/",
        "/cpp-tutorial/global-random-numbers-random-h/",
    ],
    "chapter_9": [
        "/cpp-tutorial/introduction-to-testing-your-code/",
        "/cpp-tutorial/code-coverage/",
        "/cpp-tutorial/common-semantic-errors-in-c/",
        "/cpp-tutorial/detecting-and-handling-errors/",
        "/cpp-tutorial/stdcin-and-handling-invalid-input/",
        "/cpp-tutorial/assert-and-static_assert/",
    ],
    "chapter_10": [
        "/cpp-tutorial/implicit-type-conversion/",
        "/cpp-tutorial/floating-point-and-integral-promotion/",
        "/cpp-tutorial/arithmetic-conversions/",
        "/cpp-tutorial/explicit-type-conversion-casting-and-static-cast/",
        "/cpp-tutorial/typedefs-and-type-aliases/",
    ],
    "chapter_11": [
        "/cpp-tutorial/introduction-to-function-overloading/",
        "/cpp-tutorial/deleting-functions/",
        "/cpp-tutorial/default-arguments/",
    ],
    "chapter_12": [
        "/cpp-tutorial/introduction-to-pointers/",
        "/cpp-tutorial/introduction-to-references/",
        "/cpp-tutorial/introduction-to-compound-data-types/",
        "/cpp-tutorial/value-categories-lvalues-and-rvalues/",
    ],
    "chapter_13": [
        "/cpp-tutorial/unscoped-enumerations/",
        "/cpp-tutorial/introduction-to-structs-members-and-member-selection/",
    ],
    "chapter_14": [
        "/cpp-tutorial/member-functions/",
        "/cpp-tutorial/public-and-private-members-and-access-specifiers/",
        "/cpp-tutorial/access-functions/",
        "/cpp-tutorial/constructors/",
    ],
    "chapter_15": [],
    "chapter_16": [
        "/cpp-tutorial/introduction-to-containers-and-arrays/",
        "/cpp-tutorial/introduction-to-stdvector-and-list-constructors/",
    ],
    "chapter_17": [
        "/cpp-tutorial/introduction-to-stdarray/",
        "/cpp-tutorial/introduction-to-c-style-arrays/",
        "/cpp-tutorial/multidimensional-c-style-arrays/",
        "/cpp-tutorial/multidimensional-stdarray/",
    ],
    "chapter_18": [
        "/cpp-tutorial/introduction-to-iterators/",
        "/cpp-tutorial/introduction-to-standard-library-algorithms/",
    ],
    "chapter_19": [
        "/cpp-tutorial/dynamic-memory-allocation-with-new-and-delete/",
    ],
    "chapter_20": [
        "/cpp-tutorial/introduction-to-lambdas-anonymous-functions/",
    ],
    "chapter_21": [
        "/cpp-tutorial/shallow-vs-deep-copying/",
    ],
    "chapter_22": [],
    "chapter_23": [
        "/cpp-tutorial/composition/",
        "/cpp-tutorial/aggregation/",
        "/cpp-tutorial/association/",
    ],
    "chapter_24": [
        "/cpp-tutorial/introduction-to-inheritance/",
        "/cpp-tutorial/basic-inheritance-in-c/",
        "/cpp-tutorial/inheritance-and-access-specifiers/",
        "/cpp-tutorial/multiple-inheritance/",
    ],
    "chapter_25": [
        "/cpp-tutorial/virtual-functions/",
        "/cpp-tutorial/the-virtual-table/",
    ],
    "chapter_26": [
        "/cpp-tutorial/function-template-instantiation/",
    ],
    "chapter_27": [
        "/cpp-tutorial/basic-exception-handling/",
        "/cpp-tutorial/exception-dangers-and-downsides/",
    ],
    "chapter_28": [
        "/cpp-tutorial/input-and-output-io-streams/",
    ],
    "chapter_O": [
        "/cpp-tutorial/bit-flags-and-bit-manipulation-via-stdbitset/",
        "/cpp-tutorial/bitwise-operators/",
        "/cpp-tutorial/bit-manipulation-with-bitwise-operators-and-bit-masks/",
    ],
    "chapter_F": [
        "/cpp-tutorial/constexpr-functions/",
    ],
}


def fetch_page(url):
    """获取单个页面内容"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_content(html):
    """从HTML中提取主要内容"""
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # 找到主要内容区域
    main_content = (
        soup.find("article") or soup.find("main") or soup.find("div", class_="content")
    )

    if not main_content:
        return None

    # 提取标题
    title = soup.find("h1")
    title_text = title.get_text(strip=True) if title else "Untitled"

    # 提取正文（排除导航、评论等）
    # 移除不需要的元素
    for element in main_content.find_all(
        ["nav", "script", "style", "footer", "aside", "comments"]
    ):
        element.decompose()

    # 获取文本
    text = main_content.get_text(separator="\n", strip=True)

    return f"# {title_text}\n\n{text}"


def save_content(content, filepath):
    """保存内容到文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {filepath}")


def main():
    """主函数"""
    print("LearnCpp Content Downloader")
    print("=" * 50)

    for chapter, urls in CHAPTERS.items():
        if not urls:  # Skip empty chapters
            continue

        print(f"\nDownloading {chapter}...")
        chapter_dir = os.path.join(OUTPUT_DIR, chapter)
        os.makedirs(chapter_dir, exist_ok=True)

        for url_path in urls:
            url = BASE_URL + url_path
            filename = url_path.strip("/").split("/")[-1] + ".md"
            filepath = os.path.join(chapter_dir, filename)

            # Skip if file already exists
            if os.path.exists(filepath):
                print(f"  Skipping (exists): {url_path}")
                continue

            print(f"  Fetching: {url_path}")
            html = fetch_page(url)

            if html:
                content = extract_content(html)
                if content:
                    save_content(content, filepath)

            # 礼貌性延迟
            time.sleep(1)

    print("\nDownload complete!")


if __name__ == "__main__":
    main()
