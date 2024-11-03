# 遍历../../Notes当中的所有文件，获取所有markdown文件的 YAML Front Matter

import re
import os
file_path = "/Users/kuuga/code/Notes/"
post_path = "/Users/kuuga/code/kamenriderkuuga.github.io/_posts"
cp_img_path = "/Users/kuuga/code/kamenriderkuuga.github.io/assets/img"
img_path = "/assets/img"

all_should_be_published = []


def get_yaml_front_matter(file_path):
    global all_should_be_published
    with open(file_path, "r") as f:
        content = f.read()
        pattern = re.compile(r"---\n(.*?)\n---", re.S)
        result = pattern.search(content)
        if result:
            data = result.group(1)
            if (not "excalidraw" in data):
                front_matter_dict = {}
                for line in data.split("\n"):
                    key_value = line.split(": ")
                    if len(key_value) == 2:
                        front_matter_dict[key_value[0].strip()
                                          ] = key_value[1].strip()
                    if "publish" in line:
                        all_should_be_published.append(
                            (file_path, front_matter_dict))


def get_all_files(file_path):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith(".md"):
                yield os.path.join(root, file)


for file in get_all_files(file_path):
    get_yaml_front_matter(file)

the_key_must_have = ["publish", "layout",
                     "title", "date", "author", "tags", "category"]


def check_front_matter(front_matter):
    for key in the_key_must_have:
        if key not in front_matter:
            return False
    return True


# 匹配像![](java-async-1.png)这样的图片链接
# 匹配像![[java-async-5.excalidraw.md|800]]这样的excalidraw链接
def replace_content_and_copy_assets(file, content, new_file_name):
    # get file folder
    folder = os.path.dirname(file)
    img_pattern = re.compile(r"!\[\]\((.*?)\)")
    result = img_pattern.findall(content)
    for img in result:
        # check if file exists
        if not os.path.exists(os.path.join(folder, img)):
            print(f"{img} not exists")
            return ""
    excalidraw_pattern = re.compile(r"!\[\[(.*?)\|.*?\]\]")
    excalidraw_result = excalidraw_pattern.findall(content)
    for excalidraw in excalidraw_result:
        # check if file exists
        excalidraw_svg = excalidraw.replace(".md", ".svg")
        if not os.path.exists(os.path.join(folder, excalidraw_svg)):
            print(f"{excalidraw} not exists")
            return ""
        
    # replace content
    for img in result:
        # get image file name
        img_file_name = os.path.basename(img)
        new_img_file_name = f"{new_file_name.split('.')[0]}-{img_file_name}"
        os.system(f"cp {os.path.join(folder, img)} {cp_img_path}/{new_img_file_name}")
        # replace content use img_pattern
        content = content.replace(f"({img})", f"({img_path}/{new_img_file_name})")

    for excalidraw in excalidraw_result:
        # get excalidraw file name
        excalidraw_svg = excalidraw.replace(".md", ".svg")
        excalidraw_svg_file_name = os.path.basename(excalidraw_svg)
        new_excalidraw_svg = f"{new_file_name.split('.')[0]}-{excalidraw_svg_file_name}"
        os.system(f"cp {os.path.join(folder, excalidraw_svg)} {cp_img_path}/{new_excalidraw_svg}")
        # replace content use excalidraw_pattern
        pattern = re.compile(rf"!\[\[{excalidraw}\|.*?\]\]")
        content = re.sub(pattern, f"![]({img_path}/{new_excalidraw_svg})", content)

    # replace the ```erlang with {% highlight erlang %} and {% endhighlight %}
    if "```erlang" in content:
        # Use regex to find erlang code blocks and add {% raw %} and {% endraw %}
        erlang_pattern = re.compile(r"```erlang(.*?)```", re.S)
        content = erlang_pattern.sub(r"```erlang\n{% raw %}\1{% endraw %}\n```", content)

    return content


for file, front_matter in all_should_be_published:
    if check_front_matter(front_matter):
        date = front_matter["date"]
        category = front_matter["category"]
        number = 1
        new_file_name = f"{date}-{category}-{number}.md"
        print(f"{file} should be published as {new_file_name}")
        # copy file to post_path
        with open(file, "r") as f:
            content = f.read()
            # file content replace
            content = replace_content_and_copy_assets(file, content, new_file_name)
            if content == "":
                print(f"{file} has some error in content")
            else:
                with open(os.path.join(post_path, new_file_name), "w") as f2:
                    f2.write(content)
    else:
        print(f"{file} has some error in front matter: {front_matter}")
        print("Please check it and fix it")
        break
