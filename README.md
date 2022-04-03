# COVID19-China-DailyCheck

获取新冠中高风险地区数据，记录每日变化。

## Feature

> 从[国家卫生健康委](http://bmfw.www.gov.cn/yqfxdjcx/risk.html)网站自动下载疫情风险等级数据，并保存为 *.js* 文件
> 调用check方法保存当日中高风险地区（默认）
> 调用comparsion方法自动比较最新的数据和 *Archive* 文件夹里上一份数据的不同，并标记 `removed` 或 `new` 以表示调低或新增的地区（**如果原始文件中没有多余数据会报错**）

## Usage

在 *getAdd.py* 主函数中修改合适的方法并运行，结果文件会以 *.csv* 格式直接保存在 *Archive* 文件夹里。

## About the *token* and *key* in the code


在运行程序向网站提交请求时，你会发现代码里有一些看起来像是 `token` 或者 `key` 的秘钥。这些其实都是原网站 JavaScript 代码里的明文。直接使用即可。

## OS Support

程序使用MAC进行开发，这也意味着代码路径支持linux和macos,win用户只需修改代码中的路径符'/'为'\\\\'即可使用。


