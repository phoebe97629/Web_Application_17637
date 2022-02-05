let stack = ['0']
let entering = true

function change_color(){
if (entering){document.getElementById("output").style.backgroundColor = '#f1dfcf'}
else{
if (document.getElementById("output").innerHTML=== 'divide by zero' || document.getElementById("output").innerHTML=== 'stack overflow' || document.getElementById("output").innerHTML=== 'stack underflow'){document.getElementById("output").style.backgroundColor = '#5C2223'}else{document.getElementById("output").style.backgroundColor = '#D8E2DA'}}}


function init(){
   stack = ['0']
   entering = true
   let inputElement = document.getElementById("output")
   inputElement.innerHTML = 0
   }


function input(buttonElement) {
  let init = buttonElement.innerHTML
  let inputElement = document.getElementById("output")
  let oldVal = inputElement.innerHTML
  if (entering == true){if (oldVal === '0'){
      let newVal = init
      inputElement.innerHTML = newVal
      stack.pop()
      stack.push(newVal)
      }
  else{
      let newVal = oldVal + init
      inputElement.innerHTML = newVal
      stack.pop()
      stack.push(newVal)
      }
  }
  else if (entering === false && inputElement.innerHTML === 'divide by zero'){
  let newVal = init
  inputElement.innerHTML = newVal
  stack.pop()
  stack.push(newVal)

  entering = true}
  else if (entering === false && inputElement.innerHTML === 'stack underflow'){
  let newVal = init
  inputElement.innerHTML = newVal
  stack.pop()
  stack.push(newVal)

  entering = true}
  else if (entering === false && inputElement.innerHTML === 'stack overflow'){
  let newVal = init
  inputElement.innerHTML = newVal
  stack.pop()
  stack.push(newVal)

  entering = true}
  else{
  let newVal = init
  inputElement.innerHTML = newVal

  stack.push(newVal)

  entering = true}}


 function push(){
   let numbers = document.getElementById("output")
   let num = numbers.innerHTML
   if (stack.length === 3){
   init()
   numbers.innerHTML = 'stack overflow'
   entering = false

   }
   else{
   numbers.innerHTML = '0'
   stack.push(0)
   entering = true
   }}

 function add(){
   let numbers = document.getElementById("output")

   if (entering){
   if (stack.length <2){
   init()
   numbers.innerHTML = 'stack underflow'
   entering = false}
   else{
   let y = parseInt(stack[stack.length-1])
   let x = parseInt(stack[stack.length-2])
   result = x+y
   stack.pop()
   stack.pop()
   stack.push(result)
   numbers.innerHTML = result
   entering = false
   }
   }else{
   if (stack.length <2){
   init()
   numbers.innerHTML = 'stack underflow'
   entering = false}
   else {
   let y = parseInt(stack[stack.length-1])
   let x = parseInt(stack[stack.length-2])

   result = x+y
   stack.pop()
   stack.pop()
   stack.push(result)
   numbers.innerHTML = result
   entering = false
   }}

   }

 function minus(){
   let numbers = document.getElementById("output")

   if (entering){
   if (stack.length <2){
   init()
   numbers.innerHTML = 'stack underflow'
   entering = false}
   else{
   let y = parseInt(stack[stack.length-1])
   let x = parseInt(stack[stack.length-2])
   result = x-y
   stack.pop()
   stack.pop()
   stack.push(result)
   numbers.innerHTML = result
   entering = false
   }
   }else{
   if (stack.length <2){
   init()
   numbers.innerHTML = 'stack underflow'
   entering = false}
   else {
   let y = parseInt(stack[stack.length-1])
   let x = parseInt(stack[stack.length-2])

   result = x-y
   stack.pop()
   stack.pop()
   stack.push(result)
   numbers.innerHTML = result
   entering = false
   }}

   }


 function times(){
   let numbers = document.getElementById("output")

   if (entering){
   if (stack.length <2){
   init()
   numbers.innerHTML = 'stack underflow'
   entering = false}
   else{
   let y = parseInt(stack[stack.length-1])
   let x = parseInt(stack[stack.length-2])
   result = x*y
   stack.pop()
   stack.pop()
   stack.push(result)
   numbers.innerHTML = result
   entering = false
   }
   }else{
   if (stack.length <2){
   init()
   numbers.innerHTML = 'stack underflow'
   entering = false}
   else {
   let y = parseInt(stack[stack.length-1])
   let x = parseInt(stack[stack.length-2])

   result = x*y
   stack.pop()
   stack.pop()
   stack.push(result)
   numbers.innerHTML = result
   entering = false
   }}

   }


 function divide(){
   let numbers = document.getElementById("output")

   if (entering){
   if (stack.length <2){
   init()
   numbers.innerHTML = 'stack underflow'
   entering = false}
   else{
   let y = parseInt(stack[stack.length-1])
   let x = parseInt(stack[stack.length-2])
   if (y === 0){init()
   numbers.innerHTML = 'divide by zero'
   entering = false}else{
   result = Math.floor(x/y)
   stack.pop()
   stack.pop()
   stack.push(result)
   numbers.innerHTML = result
   entering = false
   }}
   }
   else{if (stack.length <2){
   init()
   numbers.innerHTML = 'stack underflow'
   entering = false}
   else{
   let y = parseInt(stack[stack.length-1])
   let x = parseInt(stack[stack.length-2])
   if (y === 0){init()
   numbers.innerHTML = 'divide by zero'
   entering = false}else{
   result = Math.floor(x/y)
   stack.pop()
   stack.pop()
   stack.push(result)
   numbers.innerHTML = result
   entering = false
   }}}

   }