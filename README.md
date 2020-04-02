# [CS420] Compilier Design
Mini C-language interpreter implementation for KAIST CS420 course, Fall 2018. ([ppt](https://drive.google.com/file/d/1YvS2bxD74ZTghHb_67wJYngVgxtDmLZy/view?usp=sharing))

## Project implementation
### Commands
* `next`
   * Execute a single or multiple line(s) of source code.
   * _Ex)_ `next`: executes current line
   * _Ex)_ `next 10`: executes 10 lines, including current line
* `print`
   * Prints current value of variable.
   * _Ex)_ `print i`: prints value of `i`
* `trace`
   * Prints history of a variable from beginning of source code to current moment.
   * _Ex)_ `trace i`: prints history of variable `i`. For instance,
      ```
      i = N/A at line 12
      i = 0 at line 19
      i = 1 at line 19
      i = 2 at line 19
      i = 3 at line 19
### Interpretation
* Interprets this [code](https://github.com/dhsmf1416/vokpiler/blob/master/input.txt).

### Other
* Recursive function call
   * Interprets recursive function `sum` of this [code](https://github.com/dhsmf1416/vokpiler/blob/master/input1.txt).
* Run-time error handling
   * At runtime, while interpreting the source code with `next` command, when error occurs then the following message is printed and the execution is terminated.
   ```
   Run-time error : line x    // x: line number where error occurs
## Contributors
* Chanwook Lee
* Yoontaek Lee - [dhsmf1416](https://github.com/dhsmf1416)
* Doheon Hwang - [hdh112](https://github.com/hdh112)
