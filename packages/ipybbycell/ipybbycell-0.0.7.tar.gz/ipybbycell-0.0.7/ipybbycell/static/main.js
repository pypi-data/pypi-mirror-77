define(['base/js/namespace', 'jquery'], function (Jupyter, $) {
  var insert_code_cell_below = function (code) {
    Jupyter.notebook.insert_cell_below('code').set_text(code);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);
  };

  var insert_markdown_cell_below = function (md) {
    Jupyter.notebook.insert_cell_below('markdown').set_text(md);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);
  };

  var add_bby_step_desc_cells = function () {
    insert_markdown_cell_below(`### 步骤标题`);

    insert_code_cell_below(`#platform-desc
from ipyaliplayer import Player
Player(vid='--替换你的视频id，上传地址 https://www.boyuai.com/elites/admin/public-video', aspect_ratio=4/3)
`);

    insert_markdown_cell_below(`<!--步骤描述 -->

#### 知识点
- 总结视频中的知识点

#### 代码练习说明
- 代码练习题目说明

#### 代码练习提示
- 代码练习提示`);
  };

  var add_bby_string_step = function () {
    add_bby_step_desc_cells();

    insert_code_cell_below(`#platform-lock-hidden

# platform-lock-hidden 的代码不会展示，但会被运行

def add(x):
    return x + 1`);

    insert_code_cell_below(`#platform-edit

# platform-edit 可被学员编辑

$$$`);

    insert_code_cell_below(`#platform-edit-answer

# 练习答案代码
# 我们提供“一键填入”功能将答案复制到对应的代码块中
# 建议 platform-edit-answer 块是直接在 platform-edit 块的基础上修改，并添加额外的解释说明

x = add(0)`);
    insert_code_cell_below(`#platform-lock

# platform-lock 的代码会被展示和运行，无法修改
print("add(0) =", x)`);

    insert_markdown_cell_below(`add(0) = 1`);
  };

  var add_bby_lesson = function () {
    Jupyter.notebook.insert_cell_below('markdown').set_text(`## 单元标题

单元简介（目前不展示这部分，所以可以写的简单一点）`);
    Jupyter.notebook.delete_cells();

    add_bby_string_step();
  };

  var add_bby_verify_step = function () {
    add_bby_step_desc_cells();

    insert_code_cell_below(`#platform-edit

def add(x):
    return x`);

    insert_code_cell_below(`#platform-edit-answer

def add(x):
    return x + 1`);

    insert_code_cell_below(`#platform-lock
print(add(1))`);
    insert_code_cell_below(`#platform-verify
import json
if add(2) == 3 and add(-1) == 0: 
    print(json.dumps({"result": True, "displayResult": "good"}))
else:
    print(json.dumps({"result": False, "displayResult": "bad"}))`);
  };

  var add_matplotlib_step = function () {
    add_bby_step_desc_cells();

    insert_code_cell_below(`#platform-edit

import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.show()`);

    insert_code_cell_below(`#platform-edit-answer

import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.show()`);

    insert_code_cell_below(`#platform-lock-hidden

# 不要修改
print("#matplotlib#")`);

    insert_markdown_cell_below(`#matplotlib#`);
  };

  var add_turtle_step = function () {
    add_bby_step_desc_cells();

    insert_code_cell_below(`#platform-lock
from ipyturtle2 import TurtleWidget

t = TurtleWidget()
t`);

    insert_code_cell_below(`#platform-edit

t.forward(100)
t.left(90)
t.pencolor('red')
t.forward(100)
t.left(90)
t.forward(100)
t.left(90)
t.forward(100)`);

    insert_code_cell_below(`#platform-edit-answer

t.forward(100)
t.left(90)
t.pencolor('blue')
t.forward(100)`);

    insert_code_cell_below(`#platform-lock-hidden

# 不要修改
print("#turtle#")`);

    insert_markdown_cell_below(`#turtle#`);
  };

  var quizString = `#platform-quiz
import ipyquiz
quizzes = []

quizzes.append({
    "id": "fill-1",
    "type": "FILL",
    "title": "学习是系统通过____提升性能的过程。",
    "answer": "经验"
})

quizzes.append({
    "id": "fill-2",
    "type": "FILL",
    "title": """
试试**markdown**吧  
$x+1$
""",
    "answer": "1"
})

quizzes.append({
    "id": "fill-3",
    "type": "FILL",
    "title": "填啥都行",
    "answer": ""
})

quizzes.append({
    "id": "choice-1",
    "type": "SELECT",
    "title": "matplotlib 绘制图形的基本组成包含文字部分和图形部分，以下说法错误的是：",
    "answer": "1",
    "options": [
        {
            "value": "0",
            "text": "图形标题、图例是基本组成中的文字部分。"
        },
        {
            "value": "1",
            "text": "x、y 坐标轴、刻度标签是基本组成中的文字部分。"
        },
        {
            "value": "2",
            "text": "边框、网格是基本组成中的图形部分。"
        },
        {
            "value": "3",
            "text": "数据图形（折线图及散点图）是基本组成中的图形部分。"
        },
    ]
})

quizzes.append({
    "id": "choice-2",
    "type": "SELECT",
    "title": "以下关于 matplotlib 绘制图形的层次的说法，错误的是：",
    "answer": "3",
    "options": [
        {
            "value": "0",
            "text": "画架层（canvas）类似于在绘画时需要一个画架放置画板。"
        },
        {
            "value": "1",
            "text": "画板层（figure）是指在画板上可以铺上画纸，是允许绘图的最大空间"
        },
        {
            "value": "2",
            "text": "画纸层（axes）上可以进行各种图形的绘制，图形的组成元素在画纸上体现"
        },
        {
            "value": "3",
            "text": "画板层（figure）可以包含一张画纸绘制单个图，但是无法包含多张画纸绘制多个子图或者图中图。"
        },
    ]
})



ipyquiz.QuizWidget(value=quizzes, quiz_id="__ipyquiz_quiz_id")
`;

  var add_quiz_step = function () {
    insert_markdown_cell_below(`### 步骤标题`);

    insert_code_cell_below(`#platform-desc
from ipyaliplayer import Player
Player(vid='--替换你的视频id，上传地址 https://www.boyuai.com/elites/admin/public-video', aspect_ratio=4/3)
`);

    insert_markdown_cell_below(`<!--步骤描述 -->

#### 知识点
- 总结视频中的知识点`);
    insert_code_cell_below(quizString);
  };

  var add_file_cell = function () {
    insert_code_cell_below(`#platform-lock-hidden

import os
# basepath与惠楚确认
basepath = os.path.expanduser('~/share/bby/')

# 以下2选1, 请阅读波波鱼对接文档
#os.chdir(basepath)
#filepath = os.path.join(basepath, 'test.txt')`);
  };

  var addButtons = function () {
    Jupyter.toolbar.add_buttons_group([
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add BBY Lesson',
          icon: 'fa-book',
          handler: add_bby_lesson,
        },
        'add-lesson',
        'ipybbycell'
      ),
    ]);
    Jupyter.toolbar.add_buttons_group([
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add BBY String Step',
          icon: 'fa-font',
          handler: add_bby_string_step,
        },
        'add-string-step',
        'ipybbycell'
      ),
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add BBY Verify Step',
          icon: 'fa-columns',
          handler: add_bby_verify_step,
        },
        'add-verify-step',
        'ipybbycell'
      ),
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add BBY Matplotlib Step',
          icon: 'fa-area-chart',
          handler: add_matplotlib_step,
        },
        'add-matplotlib-step',
        'ipybbycell'
      ),
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add BBY Turtle Step',
          icon: 'fa-pencil',
          handler: add_turtle_step,
        },
        'add-turtle-step',
        'ipybbycell'
      ),
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add BBY Quiz Step',
          icon: 'fa-question-circle',
          handler: add_quiz_step,
        },
        'add-Quiz-Step',
        'ipybbycell'
      ),
    ]);

    Jupyter.toolbar.add_buttons_group([
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add BBY File Upload Cell',
          icon: 'fa-file',
          handler: add_file_cell,
        },
        'add-Quiz-Cell',
        'ipybbycell'
      ),
    ]);
  };

  function add_help_menu_item() {
    if ($('#jupyter_bby_help').length > 0) {
      return;
    }
    var menu_item = $('<li/>').append(
      $('<a/>')
        .html('波波鱼文档')
        .attr('title', '波波鱼文档')
        .attr('id', 'jupyter_bby_help')
        .attr('href', 'https://shimo.im/docs/dcHKYtgtXvwJQ6kC')
        .attr('target', '_blank')
        .append($('<i/>').addClass('fa fa-external-link menu-icon pull-right'))
    );
    menu_item.insertBefore($($('#help_menu > .divider')[1]));
  }
  function load_ipython_extension() {
    addButtons();
    add_help_menu_item();
  }
  return {
    load_ipython_extension: load_ipython_extension,
  };
});
