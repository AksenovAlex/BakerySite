const plus = document.querySelector('.plus'),
minus = document.querySelector('.minus'),
num = document.querySelector('.num'),
price = document.querySelector('.price')
total_price = parseInt(document.querySelector('.price').textContent);
diffprice = parseInt(document.querySelector('.price').textContent)

let a = 1

function add() {
    a++;
    total_price = total_price + diffprice;
    num.innerText = a;
    price.innerText = total_price;
    console.log(a);
    console.log(total_price);
};

function sub() {
    if(a > 1){
    a--;
    total_price = total_price - diffprice;
    num.innerText = a;
    price.innerText = total_price;
    console.log(a);
    console.log(total_price);
    }
};

plus.addEventListener('click', add, false);

minus.addEventListener('click', sub, false)

