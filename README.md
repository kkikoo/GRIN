# GRIN
实现一个GRIN语言的Interpreter - 即可以把GRIN转换为Python执行

思路分析：

GRIN Lexemes: 
组成编程语言的基本语义单元，理解为Programming Language的Atoms
GRIN中有8种Lexemes:Integer literals、Floating-point literals、String literals，Identifiers，Keywords，Comparison operators、Label markers、End-of-program markers

GRIN Labels: 
定义:行标识符
用法:通常在goto的时候用，如果没有label就只能跳转到行数，label可以将行数赋予特别的意义

GRIN Spacing: 
1. 不能有空行
2. Lexeme必须用空格隔开，空格数量不限
3. 一句话必须占一行

GRIN GOTO语法
GOTO + 数字: 去往当前行数 + 数字行
GOTO + label: 去往label行
GOTO + variable: 将variable替换翻译成前两种

实现Interpreter Class，可以读入代码(文本文件)并能按行执行、输出结果到Python Console、如果有error，不要抛出Python exception，把错误信息在Console print里
