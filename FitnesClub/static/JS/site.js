// exercise_3
window.addEventListener('load', () => {
    const preloader = document.querySelector(".loader-container");
    const mainContent = document.querySelectorAll("after-preload");

    preloader.style.display = 'none';
    for (content of mainContent)
    {
        content.style.display = "block";
    }
});



document.addEventListener("DOMContentLoaded", () => {
    console.log(window.location.pathname)

    // exercise_
    if (window.location.pathname === '/home/')
    {
        console.log("age");
        checkStorageAge();
    }
    // exercise_1
    if (window.location.pathname === '/home/')
    {
        console.log("slider");
        new Slider("slider-container");
    }
    // exercise_2
    if (window.location.pathname === '/home/')
    {
        console.log("timer")
        initializeCountdown();
    }
    // exercise_8
    if (window.location.pathname === '/home/')
    {
        // Параллакс
        const dumbbellLeft = document.getElementById("dumbbell-left");
        const dumbbellRight = document.getElementById("dumbbell-right");
        const scales = document.getElementById("scales");

        window.addEventListener("scroll", function () {
            const scrollValue = window.scrollY;

            dumbbellLeft.style.transform = `translateX(-${scrollValue * 0.8}px)`;
            dumbbellRight.style.transform = `translateX(${scrollValue * 0.8}px)`;

            const scaleValue = 1 + scrollValue * 0.0005;
            scales.style.transform = `scale(${scaleValue})`;
        });


        const wheel = document.querySelector(".wheel");

        // WEB Animation API
        const rollingAnimation = wheel.animate([
            { transform: "translateX(0vw) rotate(0deg)" },
            { transform: "translateX(100vw) rotate(720deg)" },
            { transform: "translateX(0vw) rotate(0deg)" },
        ], {
            duration: 6000,
            iterations: Infinity,
            easing: "linear"
        });

        rollingAnimation.play();
    }
    // exercise_8
    if (window.location.pathname === "/home/polygon2/")
    {
        const batteryStatusElement = document.getElementById("battery-status");

        if ('getBattery' in navigator) {
            navigator.getBattery().then(battery => {

                const updateBatteryStatus = () => {
                    const level = Math.floor(battery.level * 100);
                    const charging = battery.charging ? "Charging" : "Not charging";
                    batteryStatusElement.textContent = `Battery level: ${level}% (${charging})`;
                };

                updateBatteryStatus();

                battery.addEventListener('levelchange', updateBatteryStatus);
                battery.addEventListener('chargingchange', updateBatteryStatus);
            });
        } else {
            batteryStatusElement.textContent = "Battery Status API is not supported in this browser.";
        }
    }
    // exercise_5
    if (window.location.pathname === "/fitness/workouts/")
    {
        console.log("workouts");
        const workouts = document.querySelectorAll('.workout');

        workouts.forEach(workout => {
            workout.addEventListener('mousemove', (e) => {
                const { offsetWidth: width, offsetHeight: height } = workout;
                const { offsetX: x, offsetY: y } = e;

                const xNorm = (x / width) * 2 - 1; // от -1 до 1
                const yNorm = (y / height) * 2 - 1; // от -1 до 1

                const tiltX = -yNorm * 8; // угол наклона по Y
                const tiltY = xNorm * 8; // угол наклона по X

                workout.style.transform = `perspective(600px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
            });

            workout.addEventListener('mouseleave', () => {
                workout.style.transform = 'perspective(500px) rotateX(0deg) rotateY(0deg)';
            });

        });
    }
});


// exercise_1
class Slider {
    constructor(container) {
        this.container = document.getElementById(container);
        this.wrapper = this.container.querySelector("#slider-wrapper");
        this.slides = this.wrapper.querySelectorAll(".slide");
        this.caption = this.container.querySelector("#slide-caption");
        this.counter = this.container.querySelector("#slide-counter");
        this.pagination = this.container.querySelector("#pagination");
        this.currentIndex = 0;
        this.form = document.getElementById("slider-settings");
        this.auto = true;
        this.loop = true;
        this.navs = true;
        this.pags = true;
        this.stopMouseHover = true;
        this.delay = 5000;

        this.init();
    }

    init() {
        if (this.form)
        {
            this.auto = document.getElementById("auto").checked;
            this.loop = document.getElementById("loop").checked;
            this.navs = document.getElementById("navs").checked;
            this.pags = document.getElementById("pags").checked;
            this.delay = parseInt(document.getElementById("delay").value) * 1000;
            this.stopMouseHover = document.getElementById("stopMouseHover").checked;
        }
        this.updateSlide();
        this.updateControls();
        if (this.auto)
        {
            this.startAutoSlide();
        }
        this.attachEventListeners();
    }

    attachEventListeners() {
        if (this.form)
        {
            this.form.addEventListener("change", () => this.updateSettings());
        }
        this.container.querySelector("#next-slide").addEventListener("click", () => this.nextSlide());
        this.container.querySelector("#prev-slide").addEventListener("click", () => this.prevSlide());
        this.container.addEventListener("mouseover", () => this.pauseAutoSlide());
        this.container.addEventListener("mouseleave", () => this.resumeAutoSlide());
    }

    updateSettings() {
        if (this.form) {
            this.auto = document.getElementById("auto").checked;
            this.loop = document.getElementById("loop").checked;
            this.navs = document.getElementById("navs").checked;
            this.pags = document.getElementById("pags").checked;
            this.delay = parseInt(document.getElementById("delay").value) * 1000 || 5000;
            this.stopMouseHover = document.getElementById("stopMouseHover").checked;
            this.updateControls();

            if (this.auto) {
                this.startAutoSlide();
            } else {
                this.pauseAutoSlide();
            }
        }
    }

    updateControls() {
        this.container.querySelector("#next-slide").style.display = this.navs ? "block" : "none";
        this.container.querySelector("#prev-slide").style.display = this.navs ? "block" : "none";
        this.pagination.innerHTML = '';
        if (this.pags) this.initPagination();
    }

    updateSlide() {
        this.slides.forEach((slide, index) => {
            slide.classList.toggle("active", index === this.currentIndex);
        });
        this.caption.textContent = this.slides[this.currentIndex].dataset.caption;
        this.counter.textContent = `${this.currentIndex + 1}/${this.slides.length}`;
        Array.from(this.pagination.children).forEach((btn, index) => {
            btn.classList.toggle("active", index === this.currentIndex);
        });
    }

    nextSlide() {
        if (this.currentIndex < this.slides.length - 1) {
            this.currentIndex++;
        } else if (this.loop) {
            this.currentIndex = 0;
        }
        this.updateSlide();
    }

    prevSlide() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
        } else if (this.loop) {
            this.currentIndex = this.slides.length - 1;
        }
        this.updateSlide();
    }

    initPagination() {
        for (let i = 0; i < this.slides.length; i++) {
            const btn = document.createElement("button");
            btn.addEventListener("click", () => {
                this.currentIndex = i;
                this.updateSlide();
            });
            this.pagination.appendChild(btn);
        }
    }

    startAutoSlide() {
        clearInterval(this.autoSlideInterval);
        this.autoSlideInterval = setInterval(() => this.nextSlide(), this.delay);
    }

    pauseAutoSlide() {
        if (this.stopMouseHover && this.auto) clearInterval(this.autoSlideInterval);
        if (this.navs) document.getElementById("prev-slide").style.display = "block";
        if (this.navs) document.getElementById("next-slide").style.display = "block";
    }

    resumeAutoSlide() {
        if (this.stopMouseHover && this.auto) this.startAutoSlide();
        if (this.navs) document.getElementById("prev-slide").style.display = "none";
        if (this.navs) document.getElementById("next-slide").style.display = "none";
    }
}



// exercise_2
function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = name + '=' + encodeURIComponent(value) + '; expires=' + expires + '; path=/';
}

function getCookie(name) {
    return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
}

function deleteCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
}

function initializeCountdown() {
    const countdownElement = document.getElementById("countdown-timer");
    const oneHour = 3600 * 1000;
    let endTime = getCookie("countdownEndTime");

    if (!endTime) {
        endTime = Date.now() + oneHour;
        setCookie("countdownEndTime", endTime, 1);
    } else {
        endTime = parseInt(endTime);
    }

    function updateCountdown() {
        const now = Date.now();
        const timeLeft = endTime - now;

        if (timeLeft <= 0) {
            countdownElement.textContent = "Время истекло!";
            deleteCookie("countdownEndTime");
            return;
        }

        const hours = Math.floor(timeLeft / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        countdownElement.textContent = `${hours} : ${minutes} : ${seconds}`;
        countdownElement.style.fontSize = `30px`;
    }

    updateCountdown();
    const countdownInterval = setInterval(updateCountdown, 1000);
}



// exercise_6
function checkStorageAge() {
    if (localStorage.getItem("userAge"))
    {
        for (content of document.querySelectorAll('.main-content'))
        {
            content.style.display = 'block';
        }
        if (document.getElementById('check-birthday-date'))
        {
            document.getElementById('check-birthday-date').style.display = 'none';
        }
    }
}

function checkAge() {
    const birthdateInput = document.getElementById("birthdate").value;

    // Проверка, что дата введена
    if (!birthdateInput) {
        alert("Пожалуйста, введите дату рождения.");
        return;
    }

    const birthDate = new Date(birthdateInput);
    const today = new Date();

    // Рассчёт возраста
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDifference = today.getMonth() - birthDate.getMonth();
    const dayDifference = today.getDate() - birthDate.getDate();

    // Корректировка возраста, если день рождения в этом году ещё не наступил
    if (monthDifference < 0 || (monthDifference === 0 && dayDifference < 0)) {
        age--;
    }

    const daysOfWeek = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
    const dayOfWeek = daysOfWeek[birthDate.getDay()];

    if (age >= 18) {
        alert(`Ваша дата рождения пришлась на ${dayOfWeek}. Вам ${age} лет.`);

        for (content of document.querySelectorAll('.main-content'))
        {
            content.style.display = 'block';
            console.log(content);
            console.log("mama");
        }
        document.getElementById('check-birthday-date').style.display = 'none';

        localStorage.setItem("userAge", age);
    } else {
        alert(`Ваша дата рождения пришлась на ${dayOfWeek}. Вам ${age} лет. Необходимо разрешение родителей для использования этого сайта.`);
    }
}



// exercise_7

// В функциональном стиле
//function Person(surname, name, patronymic) {
//    this.surname = surname;
//    this.name = name;
//    this.patronymic = patronymic;
//}
//
//Person.prototype.getFullName = function() {
//    return `${this.surname} ${this.name} ${this.patronymic}`;
//};
//
//function Soldier(surname, name, patronymic, age, height) {
//    Person.call(this, surname, name, patronymic); // Вызов конструктора родителя
//    this.age = age;
//    this.height = height;
//}
//
//Soldier.prototype = Object.create(Person.prototype);
//Soldier.prototype.constructor = Soldier;
//
//Soldier.prototype.getDetails = function() {
//    return `${this.getFullName()}, Возраст: ${this.age}, Рост: ${this.height} см`;
//};
//
//function MilitaryUnit() {
//    this.soldiers = [];
//}
//
//MilitaryUnit.prototype.addSoldier = function(soldier) {
//    this.soldiers.push(soldier);
//};
//
//MilitaryUnit.prototype.checkHeightDuplicates = function() {
//    const heightCounts = {};
//    for (const soldier of this.soldiers) {
//        heightCounts[soldier.height] = (heightCounts[soldier.height] || 0) + 1;
//    }
//    return Object.values(heightCounts).some(count => count >= 2);
//};
//
//MilitaryUnit.prototype.displaySoldiers = function() {
//    const soldierList = document.getElementById("soldier-list");
//    soldierList.innerHTML = '';
//    this.soldiers.forEach(soldier => {
//        const div = document.createElement('div');
//        div.textContent = soldier.getDetails();
//        soldierList.appendChild(div);
//    });
//};



// Конструкция «class» / «extends».
class Person {
    constructor(surname, name, patronymic) {
        this.surname = surname;
        this.name = name;
        this.patronymic = patronymic;
    }

    getFullName() {
        return `${this.surname} ${this.name} ${this.patronymic}`;
    }
}


class Soldier extends Person {
    constructor(surname, name, patronymic, age, height) {
        super(surname, name, patronymic);
        this.age = age;
        this.height = height;
    }

    getDetails() {
        return `${this.getFullName()}, Возраст: ${this.age}, Рост: ${this.height} см`;
    }
}


class MilitaryUnit {
    constructor() {
        this.soldiers = [];
    }

    addSoldier(soldier) {
        this.soldiers.push(soldier);
    }

    checkHeightDuplicates() {
        const heightCounts = {};
        for (const soldier of this.soldiers) {
            heightCounts[soldier.height] = (heightCounts[soldier.height] || 0) + 1;
        }

        return Object.values(heightCounts).some(count => count >= 2);
    }

    displaySoldiers() {
        const soldierList = document.getElementById("soldier-list");
        soldierList.innerHTML = '';
        this.soldiers.forEach(soldier => {
            const div = document.createElement('div');
            div.textContent = soldier.getDetails();
            soldierList.appendChild(div);
        });
    }
}


// Задача
if (window.location.pathname === '/home/polygon2/')
{
    const unit = new MilitaryUnit();

    document.getElementById("soldier-form").addEventListener("submit", function(event) {
        event.preventDefault();
        const surname = document.getElementById("surname").value;
        const name = document.getElementById("name").value;
        const patronymic = document.getElementById("patronymic").value;
        const age = parseInt(document.getElementById("age").value);
        const height = parseInt(document.getElementById("height").value);

        const soldier = new Soldier(surname, name, patronymic, age, height);
        unit.addSoldier(soldier);
        unit.displaySoldiers();

        if (unit.checkHeightDuplicates()) {
            alert('В подразделении есть хотя бы два человека одного роста!');
        }
    });

    function checkSoldiersHeight() {
        if (unit.checkHeightDuplicates())
        {
            alert('В подразделении есть хотя бы два человека одного роста!');
        }
        else
        {
            alert('В подразделении нет людей одного роста!');
        }
    }
}

//exercise_3
if (window.location.pathname === '/fitness/super_user/')
{
    document.addEventListener("DOMContentLoaded", function () {
    const addForm = document.getElementById("add-form");
    const addInstructorBtn = document.getElementById("add-instructor-btn");
    const submitInstructorBtn = document.getElementById("submit-instructor");
    const phoneInput = document.getElementById("phone-number");
    const urlInput = document.getElementById("url");
    const phoneError = document.getElementById("phone-error");
    const urlError = document.getElementById("url-error");

    function validateForm() {
        let isValid = true;

        // Поля для проверки
        const fields = ["fullname", "age", "phone-number", "url", "username", "password", "photo"];
        fields.forEach(id => {
            const input = document.getElementById(id);
            if (input)
            {
                if (!input.value || (input.type === "file" && !input.files.length)) {
                    input.style.borderColor = "red";
                    input.style.backgroundColor = "#fdd";
                    isValid = false;
                } else {
                    input.style.borderColor = "";
                    input.style.backgroundColor = "";
                }
            }
        });

        return isValid;
    }

    // Открыть форму добавления сотрудника
    addInstructorBtn.addEventListener("click", () => {
        addForm.style.display = addForm.style.display === "none" ? "block" : "none";
    });

    // Функция для проверки номера телефона
    function validatePhone(phone) {
        const phonePattern = /^(8029\d{7}|8 \(029\) \d{7}|\+375 \(29\) \d{3}-\d{2}-\d{2}|\+375 \(29\) \d{3} \d{2} \d{2})$/;
        return phonePattern.test(phone);
    }

    // Функция для проверки URL
    function validateURL(url) {
        const urlPattern = /^(https?:\/\/).*\.(php|html)$/;
        return urlPattern.test(url);
    }

    // Проверка и вывод ошибок валидации при изменении полей
    phoneInput.addEventListener("input", () => {
        if (validatePhone(phoneInput.value)) {
            phoneInput.classList.remove("error");
            phoneError.style.display = "none";
        } else {
            phoneInput.classList.add("error");
            phoneError.style.display = "block";
        }
    });

    urlInput.addEventListener("input", () => {
        if (validateURL(urlInput.value)) {
            urlInput.classList.remove("error");
            urlError.style.display = "none";
        } else {
            urlInput.classList.add("error");
            urlError.style.display = "block";
        }
    });

    const instructorForm = document.getElementById("instructor-form");
    const url = "http://127.0.0.1:8000/fitness/super_user/";

    submitInstructorBtn.addEventListener("click", async () => {

        if (!validateForm()) {
            alert("Пожалуйста, заполните все поля.");
            return;
        }

        if (validatePhone(phoneInput.value) && validateURL(urlInput.value)) {
             const formData = new FormData(instructorForm);

            try {
                const response = await fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    alert("Новый сотрудник добавлен!");
                    location.reload();
                } else {
                    const errorData = await response.json();
                    alert("Ошибка при добавлении: " + errorData.error);
                }
            } catch (error) {
                console.error("Ошибка при отправке запроса:", error);
            }
        }
        if (!validatePhone(phoneInput.value))
        {
            phoneInput.classList.add("error");
            phoneError.style.display = "block";
        }
        if (!validateURL(urlInput.value))
        {
            urlInput.classList.add("error");
            urlError.style.display = "block";
        }
    });

    // Вывод информации о сотруднике при клике на строку
    document.querySelectorAll(".instructor-row").forEach(row => {
        row.addEventListener("click", function () {
            const fullname = this.cells[0].textContent;
            const age = this.cells[2].textContent;
            const phone = this.cells[3].textContent;
            const username = this.cells[4].textContent;

            document.getElementById("detail-fullname").textContent = fullname;
            document.getElementById("detail-age").textContent = age;
            document.getElementById("detail-phone").textContent = phone;
            document.getElementById("detail-username").textContent = username;
            document.getElementById("instructor-details").style.display = "block";
        });
    });
});
}