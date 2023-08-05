define(['base/js/namespace', 'jquery'], function (Jupyter, $) {
  var add_bby_step_desc_cells = function () {
    Jupyter.notebook.insert_cell_below('markdown').set_text(`### 步骤标题`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-desc
from ipyaliplayer import Player
Player(vid='--替换你的视频id，上传地址 https://www.boyuai.com/elites/admin/public-video', aspect_ratio=4/3)
`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('markdown').set_text(`<!--步骤描述 -->
#### 【前言】
- 总结视频中的知识点
#### 【练习】
- 练习指导等内容
#### 【练习目标】
- 练习的教学目标
`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);
  };

  var add_bby_step_cells = function () {
    add_bby_step_desc_cells();

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit
# 学生实践代码
`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit-answer
# 答案代码，为本步骤的答案，我们提供“一键填入”功能，将答案复制到对应的代码块中。
# 所以建议 #platform-edit-answer 块是直接在 #platform-edit 块的基础上修改，并添加额外的解释说明。
`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);
  };

  var add_bby_lesson_cells = function () {
    Jupyter.notebook.insert_cell_below('markdown').set_text(`## 课程标题`);
    Jupyter.notebook.delete_cells();
    // Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    add_bby_step_cells();
    add_bby_step_cells();
  };

  var add_turtle_cell = function () {
    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-lock
from ipyturtle2 import TurtleWidget

t = TurtleWidget()
t`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit

t.forward(100)
t.left(90)
t.pencolor('red')
t.forward(100)
t.left(90)
t.forward(100)
t.left(90)
t.forward(100)`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit-answer

t.forward(100)
t.left(90)
t.pencolor('blue')
t.forward(100)`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-lock-hidden
print("#turtle#")`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('markdown').set_text(`#turtle#`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);
  };

  var add_matplotlib_cell = function () {
    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit

import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.show()`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit-answer

import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.show()`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-lock-hidden

print("#matplotlib#")`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('markdown').set_text(`#matplotlib#`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);
  };

  var add_string_verify_cell = function () {
    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit

print("123.")
print("testing")
print("lalala...")`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit-answer
print("123")
print("testing!")
print("lalala....")`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('markdown').set_text(`123
testing!
lalala....`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);
  };

  var add_code_verify_cell = function () {
    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit

def add(x):
    return x`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-edit-answer

def add(x):
    return x + 1`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-lock
print(add(1))`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);

    Jupyter.notebook.insert_cell_below('code').set_text(`#platform-verify
import json
if add(2) == 3 and add(-1) == 0: # 替换为你需要的判断表达式
    print(json.dumps({"result": True, "displayResult": "good"}))
else:
    print(json.dumps({"result": False, "displayResult": "bad"}))`);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);
  };

  var quizString = `
#platform-quiz
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

  var add_quiz_cell = function () {
    Jupyter.notebook.insert_cell_below('code').set_text(quizString);
    Jupyter.notebook.select(Jupyter.notebook.get_selected_index() + 1);
  };

  var add_quiz_step = function () {
    add_bby_step_desc_cells();
    add_quiz_cell();
  };

  var addButtons = function () {
    Jupyter.toolbar.add_buttons_group([
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add BBY Lesson',
          icon: 'fa-book',
          handler: add_bby_lesson_cells,
        },
        'add-lesson-cells',
        'ipybbycell'
      ),
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add BBY Step',
          icon: 'fa-map-pin',
          handler: add_bby_step_cells,
        },
        'add-step-cells',
        'ipybbycell'
      ),
    ]);
    Jupyter.toolbar.add_buttons_group([
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add Turtle Cell',
          icon: 'fa-pencil',
          handler: add_turtle_cell,
        },
        'add-turtle-cell',
        'ipybbycell'
      ),
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add Matplotlib Cell',
          icon: 'fa-area-chart',
          handler: add_matplotlib_cell,
        },
        'add-matplotlib-cell',
        'ipybbycell'
      ),
    ]);

    Jupyter.toolbar.add_buttons_group([
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add String Verify',
          icon: 'fa-font',
          handler: add_string_verify_cell,
        },
        'add-string-verify',
        'ipybbycell'
      ),
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add Code Verify',
          icon: 'fa-code',
          handler: add_code_verify_cell,
        },
        'add-code-verify',
        'ipybbycell'
      ),
    ]);

    Jupyter.toolbar.add_buttons_group([
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add Quiz Step',
          icon: 'fa-question-circle',
          handler: add_quiz_step,
        },
        'add-Quiz-Step',
        'ipybbycell'
      ),
      Jupyter.keyboard_manager.actions.register(
        {
          help: 'Add Quiz Cell',
          icon: 'fa-question-circle-o',
          handler: add_quiz_cell,
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
