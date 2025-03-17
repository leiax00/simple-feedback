/**
 * @see https://prettier.io/docs/configuration
 * @type {import("prettier").Config}
 */
export default {
  tabWidth: 2,
  semi: false,
  singleQuote: false,
  printWidth: 120,
  trailingComma: "all",
  arrowParens: "avoid", // 单个参数的箭头函数不加括号 x => x
  bracketSpacing: true, // 对象大括号内两边是否加空格 { a:0 }
  vueIndentScriptAndStyle: true, // vue文件script和style标签内的代码缩进
}
