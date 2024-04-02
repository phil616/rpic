Procedure,Function,Script的区别

Procedure: 一个过程，是一个执行过程的函数，不允许闭包，可以被挂在到一个Endpoint上
Function: 一个函数，允许闭包，但不能使用全局变量，不能被挂载到Endpoint上
Script: 一个脚本，允许闭包，直接执行

| 类型      | 闭包        | 全局环境变量         |     参数   |挂载到端点 |  最终目标形式  |
| --------- | ------------ | ---------------- | ----------  | ---------- | -------------- |
| Procedure | 不允许闭包   | 可使用           | 交换格式参数   | 可挂载         |  codeobject raw |
| Function  | 允许闭包     | 可使用           | 对象参数       | 可挂载     |  dill package   |
| Script    | 允许闭包     | 不可使用         | 不可用参数       | 不可挂载       |  str raw        |

# 内容

1. 编译器和反编译器

2. 序列化器和反序列化器

3. 加密解密和哈希模块

4. 编解码器

# 步骤

1. 编译
2. 序列化
3. 编码
4. 加密