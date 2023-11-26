# HomeWorkHelper
学生作业帮，包含文心一言应用，GPTs，以及相关插件服务


# 最终效果

## 能力

1.  回答问题会结合网络搜索的答案（具有实时性和符合标准答案），引导用户自己得出正确答案。
2.  必要时能够通过画图引导用户如何构思和解题。
3.  必要时会用代码解释器对一些数值问题进行计算。

## 效果图

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/bf5483ae28d64d718a052681ec531e9f~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=418&h=221&s=25173&e=png&b=fefefe)

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/065fda4e42584deaaf1f6086172875c4~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=772&h=571&s=120905&e=png&b=fefefe)

# 上手体验

https://chat.openai.com/g/g-rnQtJ1XIv-da-xue-sheng-zuo-ye-bang

# 阅读以下内容你将学会

1.  什么是GPTs
2.  如何快速创建GPTs引导词
3.  如何对接自定义API

# 什么是GPTs

-   GPTs是OpenAI推出ChatGPT的自定义版本，任何人都可以创建定制版本的ChatGPT，以在日常生活中、特定任务中、工作中或家庭中更有帮助，而且可以与其他人分享这一创作。例如，GPTs可以帮助你学习任何棋盘游戏的规则，帮助教孩子数学，或设计贴纸。
-   无需编码即可创建一个GPT就像开始一个对话，给它指令和额外的知识，然后选择它可以执行的操作，如搜索网页、创建图像或分析数据。
-   本月晚些时候，OpenAI将推出GPT Store，其中包括经过验证的构建者的创作。一旦进入商店，GPTs将变得可搜索，并且可能会上升到榜单中。而且诸如生产力、教育和“娱乐”等类别中将突出显示最有用和最受欢迎的GPTs。
-   在未来的几个月里，开发者还将能够根据使用自己创建的GPT的人数来赚取收益。

# 手把手创建GPTs

首先，我们进入新版的ChatGPT界面，点击Explore，点击右侧Create，如下图：

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b3713fb2c02d4319b44777ad9f8a2fb0~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=804&h=262&s=44958&e=png&b=fefefe)

进入创建页面，可以直接通过对话创建，对话方式创建本文不介绍，我们点击Configure，手动添加相关配置。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f5762fe1a43545f6a2b83f36d763f840~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=815&h=563&s=67553&e=png&b=fefefe)

对于名称，描述，Logo，预设问题，知识库，可自行添加

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/296a6c97f3bb4f05a09e06ff21ba17de~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=815&h=940&s=171765&e=png&b=fdfdfd)

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/abfa7decd0e34fe4b6dfb82b00952905~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=427&h=609&s=58720&e=png&b=fdfdfd)

# 如何创建更好的提示词？

我们可以用一个专门创建提示词的[LangGPT](https://chat.openai.com/g/g-gP24xxhB2-langgpt)（https://chat.openai.com/g/g-gP24xxhB2-langgpt）帮助我们创建：

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/47998ca864d34e66ad36e1d47aee54be~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=543&h=736&s=110167&e=png&b=fefefe)

它会以LangGPT的提示词模板给出合适的提示词，生成的提示词复制到Instructions，按需修改一下即可。

> 该GPT内置反爬提示词，防止你的提示词泄漏

  


# 如何创建Actions（自定义API插件

我们可以让创建的GPT通过API 获取外界的信息！完成各种你需要获得的数据或者第三方提供的功能。

从官方文档的设定上看，与 ChatGPT 插件一样，Action允许您将 GPT 连接到自定义 API。

我们点击Action按钮进入以下界面：

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a1cb20c8c2cc46d3bd9c3f6fc526d36f~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=817&h=938&s=170031&e=png&b=fdfdfd)

## 写一个自己的API

为了更好的介绍如何使用Action，我们这里介绍简单写一个自己的API，，如果没有编码能力可跳过此部分。

### Express

我们使用express写个简单的接口，部署过程略过，具体代码如下：

```
const express = require("express");
const { webkit } = require("playwright");
const cors = require("cors");
const app = express();
const port = 7788;
app.use(express.json());
app.use(cors());
app.use(express.static("public"));
let browser;
let context;
async function isSelectorExists(page, selector) {
  return (await page.$(selector).catch(() => null)) !== null;
}
app.get("/search", async (req, res) => {
  if (!browser | !context) {
    browser = await webkit.launch({
      headless: false,
    });
    context = await browser.newContext({ storageState: "auth.json" });
  }
  const questions = req.query.question;

  if (!questions) {
    return res.status(400).send("No questions provided");
  }
  console.log("question", questions);

  try {
    const searchList = await (
      await fetch(
        "https://easylearn.baidu.com/edu-web-go/bgk/searchlist?query=" +
          encodeURI(questions)
      )
    ).json();
    console.log("searchList", searchList.data.list[0].qid);
    const answerPage = await context.newPage();
    await answerPage.goto(
      `https://easylearn.baidu.com/edu-page/tiangong/bgkdetail?id=${searchList.data.list[0].qid}`
    );
    await answerPage.waitForSelector(".tab");
    const answerTab = await answerPage.$$(".tab-item");
    const answers = [];
    for (let i = 0; i < answerTab.length; i++) {
      await answerTab[i].click();
      if (!(await isSelectorExists(answerPage, ".question-anwser"))) {
        await answerPage.getByText("免费查看答案与解析").click();
        await answerPage.getByText("仅查看本题答案").click();
      }
      const question = await answerPage.locator(".question-stem").innerText();
      const answer = await answerPage.locator(".question-anwser").innerText();
      answers.push({ question, answer });
    }
    await answerPage.close();
    return res.status(200).json({ answers });
  } catch (error) {
    console.log("err", error);
    return res.status(200).json({ err: error.message });
  }
});
process.on("exit", async () => {
  await browser.close();
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
```

⚠️注意

1.  需要设置跨域
1.  部署时建议配置域名证书（不建议签发R3，可能会进白名单

### Laf

开发一个接口还要涉及部署等问题，还要从0写一个启动，各种配置，非常麻烦，这里推荐使用[云函数Laf平台](https://laf.run/signup?code=XlbsHlr)。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/39fe725f47114c7dbbe919a7866745eb~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1265&h=308&s=61454&e=png&b=f7f8fa)

非常快速即可开发一个小接口并部署好，具体教程可以直接进入官网查看，这里不赘述。

  


### 接口情况

我们这里写好一个接口后，我们来看一下接口如何使用。

上述express代码定义了`/search`接口，是一个`get`方法，`query`只有一个question，返回的结果和调用示例：

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9c2c9092e2b340eb870cb6e8d45e107f~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=568&h=416&s=72415&e=png&b=fdfdfd)

可以看出，传递一个问题进去，能够得到5个候选答案。

接下来，我们开始写Action必要的接口Schema，我们这里也不需要自己直接写，而是用一个专门生成JSON Schema的工具（https://chat.openai.com/g/g-5boouomxo-gpt-api-schema-builder）即可。

我们给出接口的示例和返回的示例，它就能生成schema。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b300eeb7ae0f40fda54ea49b6e270b04~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=981&h=835&s=105344&e=png&b=fefefe)

生成好之后，复制到Schema编辑框即可。

注意

每次更改schema，必须删除整个action，否则可能不会正常更新（也许是Bug

如果想要公开GPT，则必须添加隐私协议。

  


右侧可以在线调试GPT，记住，想要让GPT调用接口，除了schema的接口描述要写得好，也要在引导提示词添加相应的引导，例如让gpt每次回答前都执行Action。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d059b108df6847588e09762ce3b0eca6~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=817&h=938&s=156004&e=png&b=fdfdfd)

  


# 导出

点击右上角导出即可，可以选择公开或者分享。

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a3677d3cdaaa409cb638826482517535~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=316&h=359&s=24688&e=png&b=fcfcfc)

# 常见问题

1.  Error Talking to xxx

需仔细检查配置项是否漏填，是否网站被gpt拦截（可能是证书问题）。修改好后需要删除action重新写，否则可能不更新。


# 结语

本文来自Marlene & Idealeap
