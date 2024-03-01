
> 编译须知:可以使用arnold自带的oslc来编译
> oslc -o <output.oso> <input.osl>


OSL 包括以下类型的结构

- 范围声明
- 变量声明
- 表达式
- 赋值
- 控制流
- 函数声明

# 范围声明
在任何可以使用语句的地方，都可以使用大括号`{}`来括弧多个语句。这就是所谓的作用域。在作用域中声明的任何变量或函数只能在该作用域中可见，并且只能在声明后使用。被引用的变量或函数将始终解析到与其使用相关的最内层作用域中的匹配名称。例如  
```python
float a = 1;
float b = 2;
{
    float a = 3;
    float c = 1;
    b = a;
}
b += c; //这里会报错，因为c没有定义
```
# 1.1 变量声明和赋值

## 1.1.1 声明变量

声明变量的语法如下：
```python
type name;
type name = value;
```

- 其中，`type`是变量的类型，可以是`int`，`float`，`string`，`color`，`vector`，`matrix`,`point`,`normal`,`void`
- `name`是变量的名称
- 如果要初始化变量的数值，可以立即为其赋值。

## 1.1.2 数组
```python
float d[10]; 
float c[3] = { 0.1, 0.2, 3.14 };
```
