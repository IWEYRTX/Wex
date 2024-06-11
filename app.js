document.addEventListener('DOMContentLoaded', function () {
    // Initialize AOS library
    AOS.init();

    // Initialize i18next
    i18next.use(window.i18nextBrowserLanguageDetector).init({
        fallbackLng: 'en',
        resources: {
            en: {
                translation: {
                    "nav": {
                        "home": "Home",
                        "features": "Features",
                        "download": "Download",
                        "about": "About",
                        "contact": "Contact"
                    },
                    "hero": {
                        "title": "Welcome to Wexium Linux",
                        "description": "The ultimate Linux distribution for power users and gamers.",
                        "button": "Download Now"
                    },
                    "features": {
                        "title": "Features",
                        "performance": {
                            "title": "Optimized Performance",
                            "description": "Experience a lightning-fast desktop environment optimized for performance."
                        },
                        "customizable": {
                            "title": "Customizable",
                            "description": "Highly customizable to meet your individual needs and preferences."
                        },
                        "gaming": {
                            "title": "Gaming Ready",
                            "description": "Pre-installed with all the essential tools and optimizations for gamers."
                        },
                        "Apps": {
                            "title": "Wextweaks - Wex QS",
                            "description": "Pre-installed software"
                        }
                    },
                    "download": {
                        "title": "Download Wexium Linux",
                        "description": "Choose the version that’s right for you and start your journey with Wexium Linux.",
                        "button": "Download ISO",
                    },
                    "about": {
                        "title": "About Wexium Linux",
                        "description": "Wexium Linux is a powerful, user-friendly Linux distribution designed for both power users and gamers. With its sleek design, lightweight architecture, and extensive customization options, Wexium makes using Linux enjoyable and efficient. Our mission is to provide an exceptional Linux experience that combines stability, performance, and beauty."
                    },
                }
            },
            ru: {
                translation: {
                    "nav": {
                        "home": "Главная",
                        "features": "Особенности",
                        "download": "Скачать",
                        "about": "О нас",
                        "contact": "Контакты"
                    },
                    "hero": {
                        "title": "Добро пожаловать в Wexium Linux",
                        "description": "Лучший Linux-дистрибутив для опытных пользователей и геймеров.",
                        "button": "Скачать сейчас"
                    },
                    "features": {
                        "title": "Особенности",
                        "performance": {
                            "title": "Оптимизированная производительность",
                            "description": "Наслаждайтесь быстрой и оптимизированной средой рабочего стола."
                        },
                        "customizable": {
                            "title": "Настраиваемый",
                            "description": "Высокая настраиваемость для удовлетворения ваших индивидуальных потребностей и предпочтений."
                        },
                        "gaming": {
                            "title": "Готов к играм",
                            "description": "Предустановлены все необходимые инструменты и оптимизации для геймеров."
                        },
                        "Apps": {
                            "title": "Wextweaks - Wex QS",
                            "description": "Предустановлены все программы для простоты пользования."
                        }
                    },
                    "download": {
                        "title": "Скачать Wexium Linux",
                        "description": "Выберите нужную версию и начните своё путешествие с Wexium Linux.",
                        "button": "Скачать ISO",
                    },
                    "about": {
                        "title": "О Wexium Linux",
                        "description": "Wexium Linux — это мощный, удобный Linux-дистрибутив, предназначенный как для опытных пользователей, так и для геймеров. С его стильным дизайном, легкой архитектурой и обширными параметрами настройки, использование Wexium делает Linux приятным и эффективным. Наша миссия — предоставить исключительный опыт использования Linux, сочетающий стабильность, производительность и красоту."
                    },
                }
            }
        }
    }, function (err, t) {
        if (err) console.error(err);
        // Initialize the project
        updateContent();
    });

    // Language switcher
    document.getElementById('lang-en').addEventListener('click', function () {
        i18next.changeLanguage('en', function (err, t) {
            if (err) return console.error(err);
            updateContent();
        });
    });

    document.getElementById('lang-ru').addEventListener('click', function () {
        i18next.changeLanguage('ru', function (err, t) {
            if (err) return console.error(err);
            updateContent();
        });
    });

    function updateContent() {
        jqueryI18next.init(i18next, $);
        $('body').localize();
    }
});