const express = require("express");
const { webkit } = require("playwright");
const cors = require("cors");
const app = express();
const port = 7788;
app.use(express.json());
app.use(cors());
let browser;
let context;
async function isSelectorExists(page, selector) {
  return (await page.$(selector).catch(() => null)) !== null;
}
app.get("/", (req, res) => {
  res.redirect(
    302,
    "https://github.com/MarleneJiang/HomeWorkHelper"
  );
});
app.get("/search", async (req, res) => {
  if (!browser | !context) {
    browser = await webkit.launch({
      headless: true,
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
    await answerPage.close();
    if(error.message=="browserContext.newPage: Target page, context or browser has been closed"){
        await browser.close();
        browser = await webkit.launch({
          headless: true,
        });
        context = await browser.newContext({ storageState: "auth.json" });
    }
    return res.status(200).json({ err: error.message });
  }
});
process.on("exit", async () => {
  await browser.close();
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
//npx playwright codegen -b webkit --save-storage=auth.json --load-storage=auth.json
