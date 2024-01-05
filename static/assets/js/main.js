/**
 * Template Name: Arsha
 * Updated: Jul 27 2023 with Bootstrap v5.3.1
 * Template URL: https://bootstrapmade.com/arsha-free-bootstrap-html-template-corporate/
 * Author: BootstrapMade.com
 * License: https://bootstrapmade.com/license/
 */
(function() {
    "use strict";

    /**
     * Easy selector helper function
     */
    const select = (el, all = false) => {
        el = el.trim();
        if (all) {
            return [...document.querySelectorAll(el)];
        } else {
            return document.querySelector(el);
        }
    };

    /**
     * Easy event listener function
     */
    const on = (type, el, listener, all = false) => {
        let selectEl = select(el, all);
        if (selectEl) {
            if (all) {
                selectEl.forEach((e) => e.addEventListener(type, listener));
            } else {
                selectEl.addEventListener(type, listener);
            }
        }
    };

    /**
     * Easy on scroll event listener
     */
    const onscroll = (el, listener) => {
        el.addEventListener("scroll", listener);
    };

    /**
     * Navbar links active state on scroll
     */
    let navbarlinks = select("#navbar .scrollto", true);
    const navbarlinksActive = () => {
        let position = window.scrollY + 200;
        navbarlinks.forEach((navbarlink) => {
            if (!navbarlink.hash) return;
            let section = select(navbarlink.hash);
            if (!section) return;
            if (
                position >= section.offsetTop &&
                position <= section.offsetTop + section.offsetHeight
            ) {
                navbarlink.classList.add("active");
            } else {
                navbarlink.classList.remove("active");
            }
        });
    };
    window.addEventListener("load", navbarlinksActive);
    onscroll(document, navbarlinksActive);

    /**
     * Scrolls to an element with header offset
     */
    const scrollto = (el) => {
        let header = select("#header");
        let offset = header.offsetHeight;

        let elementPos = select(el).offsetTop;
        window.scrollTo({
            top: elementPos - offset,
            behavior: "smooth",
        });
    };

    /**
     * Toggle .header-scrolled class to #header when page is scrolled
     */
    let selectHeader = select("#header");
    if (selectHeader) {
        const headerScrolled = () => {
            if (window.scrollY > 100) {
                selectHeader.classList.add("header-scrolled");
            } else {
                selectHeader.classList.remove("header-scrolled");
            }
        };
        window.addEventListener("load", headerScrolled);
        onscroll(document, headerScrolled);
    }

    /**
     * Back to top button
     */
    let backtotop = select(".back-to-top");
    if (backtotop) {
        const toggleBacktotop = () => {
            if (window.scrollY > 100) {
                backtotop.classList.add("active");
            } else {
                backtotop.classList.remove("active");
            }
        };
        window.addEventListener("load", toggleBacktotop);
        onscroll(document, toggleBacktotop);
    }

    /**
     * Mobile nav toggle
     */
    on("click", ".mobile-nav-toggle", function(e) {
        select("#navbar").classList.toggle("navbar-mobile");
        this.classList.toggle("bi-list");
        this.classList.toggle("bi-x");
    });

    /**
     * Mobile nav dropdowns activate
     */
    on(
        "click",
        ".navbar .dropdown > a",
        function(e) {
            if (select("#navbar").classList.contains("navbar-mobile")) {
                e.preventDefault();
                this.nextElementSibling.classList.toggle("dropdown-active");
            }
        },
        true
    );

    /*
     * Scrool with ofset on links with a class name .scrollto
     */
    on(
        "click",
        ".scrollto",
        function(e) {
            if (select(this.hash)) {
                e.preventDefault();

                let navbar = select("#navbar");
                if (navbar.classList.contains("navbar-mobile")) {
                    navbar.classList.remove("navbar-mobile");
                    let navbarToggle = select(".mobile-nav-toggle");
                    navbarToggle.classList.toggle("bi-list");
                    navbarToggle.classList.toggle("bi-x");
                }
                scrollto(this.hash);
            }
        },
        true
    );

    /**
     * Scroll with ofset on page load with hash links in the url
     */
    window.addEventListener("load", () => {
        if (window.location.hash) {
            if (select(window.location.hash)) {
                scrollto(window.location.hash);
            }
        }
    });

    /**
     * Preloader
     */
    let preloader = select("#preloader");
    if (preloader) {
        window.addEventListener("load", () => {
            preloader.remove();
        });
    }

    /**
     * Initiate  glightbox
     */
    const glightbox = GLightbox({
        selector: ".glightbox",
    });

    /**
     * Skills animation
     */
    let skilsContent = select(".skills-content");
    if (skilsContent) {
        new Waypoint({
            element: skilsContent,
            offset: "80%",
            handler: function(direction) {
                let progress = select(".progress .progress-bar", true);
                progress.forEach((el) => {
                    el.style.width = el.getAttribute("aria-valuenow") + "%";
                });
            },
        });
    }

    /**
     * Porfolio isotope and filter
     */
    window.addEventListener("load", () => {
        let requestContainer = select(".request-container");
        if (requestContainer) {
            let requestIsotope = new Isotope(requestContainer, {
                itemSelector: ".request-item",
            });

            let requestFilters = select("#request-flters li", true);

            on(
                "click",
                "#request-flters li",
                function(e) {
                    e.preventDefault();
                    requestFilters.forEach(function(el) {
                        el.classList.remove("filter-active");
                    });
                    this.classList.add("filter-active");

                    requestIsotope.arrange({
                        filter: this.getAttribute("data-filter"),
                    });
                    requestIsotope.on("arrangeComplete", function() {
                        AOS.refresh();
                    });
                },
                true
            );
        }
    });

    /**
     * Initiate request lightbox
     */
    const requestLightbox = GLightbox({
        selector: ".request-lightbox",
    });

    /**
     * request details slider
     */
    new Swiper(".request-details-slider", {
        speed: 400,
        loop: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        pagination: {
            el: ".swiper-pagination",
            type: "bullets",
            clickable: true,
        },
    });

    /**
     * Animation on scroll
     */
    window.addEventListener("load", () => {
        AOS.init({
            duration: 1000,
            easing: "ease-in-out",
            once: true,
            mirror: false,
        });
    });
})();

/* Added graph, table button Code*/

function accesstable() {
    // Get the table element.
    const table = document.getElementById("table");

    // Get all of the rows in the table.
    const rows = table.getElementsByTagName("tr");

    // For each row in the table,
    for (let i = 0; i < rows.length; i++) {
        // Get the cell in the row that contains the data.
        const dataCell = rows[i].getElementsByTagName("td")[0];

        // Get the data from the cell.
        const data = dataCell.innerHTML;

        // Print the data to the console.
        console.log(data);
    }
}

// When the user clicks on the "btn btn-primary" button,
// document
//     .getElementById("btn-btn-primary")
//     .addEventListener("click", accesstable);

//apex chart
//User chart
var optionsUser = {
    series: [{
        name: "Desktops",
        data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
    }],
    UserChart: {
        height: 350,
        type: 'line',
        zoom: {
            enabled: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'straight'
    },
    title: {
        text: 'Product Trends by Month',
        align: 'left'
    },
    grid: {
        row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
        },
    },
    xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
    }
};

var UserChart = new ApexCharts(document.querySelector("#UserChart"), options);
UserChart.render();

//Water Quality Chart

var optionsWater = {
    series: [{
        name: "Desktops",
        data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
    }],
    WaterQualityChart: {
        height: 350,
        type: 'line',
        zoom: {
            enabled: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'straight'
    },
    title: {
        text: 'Product Trends by Month',
        align: 'left'
    },
    grid: {
        row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
        },
    },
    xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
    }
};

var WaterQualityChart = new ApexCharts(document.querySelector("#Water-Quality-Chart"), options);
WaterQualityChart.render();

//Multi[le Charts

//Chlorine Chart
var optionsChlorine = {
    series: [{
        data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
    }],
    chlorine: {
        type: 'bar',
        height: 350,
    },
    plotOptions: {
        bar: {
            borderRadius: 4,
            horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    xaxis: {
        categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
            'United States', 'China', 'Germany'
        ],
    }
};

var chlorine = new ApexCharts(document.querySelector("#Chlorine"), options);
chlorine.render();

//Chart2
var optionsPressure = {
    series: [{
        data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
    }],
    pressure: {
        type: 'bar',
        height: 350
    },
    plotOptions: {
        bar: {
            borderRadius: 4,
            horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    xaxis: {
        categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
            'United States', 'China', 'Germany'
        ],
    }
};

var pressure = new ApexCharts(document.querySelector("#Pressure"), options);
pressure.render();

//Chart 3
var optionsBattery = {
    series: [{
        data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
    }],
    battery: {
        type: 'bar',
        height: 350
    },
    plotOptions: {
        bar: {
            borderRadius: 4,
            horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    xaxis: {
        categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
            'United States', 'China', 'Germany'
        ],
    }
};

var battery = new ApexCharts(document.querySelector("#Battery"), options);
battery.render();

//Chart4
var optionsSignal = {
    series: [{
        data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
    }],
    SignalStrength: {
        type: 'bar',
        height: 350
    },
    plotOptions: {
        bar: {
            borderRadius: 4,
            horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    xaxis: {
        categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
            'United States', 'China', 'Germany'
        ],
    }
};

var SignalStrength = new ApexCharts(document.querySelector("#SignalStrength"), options);
SignalStrength.render();



//SITE DETAILS Chart



var optionsSite = {
    series: [44, 55, 13, 33],
    SiteStatusChart: {
        width: 380,
        type: 'donut',
    },
    dataLabels: {
        enabled: false,
    },
    responsive: [{
        breakpoint: 480,
        optionsSite: {
            SiteStatusChart: {
                width: 200,
            },
        }
    }],
    legend: {
        show: false
    }
    // legend: {
    //     position: 'right',
    //     offsetY: 0,
    //     height: 230,
    // }
};

var SiteStatusChart = new ApexCharts(document.querySelector("#SiteStatusChart"), options);
SiteStatusChart.render();


function appendData() {
    var arr = SiteStatusChart.w.globals.series.slice()
    arr.push(Math.floor(Math.random() * (100 - 1 + 1)) + 1)
    return arr;
}

function removeData() {
    var arr = SiteStatusChart.w.globals.series.slice()
    arr.pop()
    return arr;
}

function randomize() {
    return SiteStatusChart.w.globals.series.map(function() {
        return Math.floor(Math.random() * (100 - 1 + 1)) + 1
    })
}

function reset() {
    return optionsSite.series
}

document.querySelector("#randomize").addEventListener("click", function() {
    SiteStatusChart.updateSeries(randomize())
})

document.querySelector("#add").addEventListener("click", function() {
    SiteStatusChart.updateSeries(appendData())
})

document.querySelector("#remove").addEventListener("click", function() {
    SiteStatusChart.updateSeries(removeData())
})

document.querySelector("#reset").addEventListener("click", function() {
    SiteStatusChart.updateSeries(reset())
})




//Device DETAILS chart




var optionsDevice = {
    series: [44, 55, 13, 33],
    deviceStatusChart: {
        width: 380,
        type: 'donut',
    },
    dataLabels: {
        enabled: false
    },
    responsive: [{
        breakpoint: 480,
        optionsDevice: {
            deviceStatusChart: {
                width: 200
            },

        }
    }],
    legend: {
        show: false
    }
    // legend: {
    //     position: 'right',
    //     offsetY: 0,
    //     height: 230,
    // }
};

var deviceStatusChart = new ApexCharts(document.querySelector("#device-Status-chart"), options);
deviceStatusChart.render();


function appendData() {
    var arr = deviceStatusChart.w.globals.series.slice()
    arr.push(Math.floor(Math.random() * (100 - 1 + 1)) + 1)
    return arr;
}

function removeData() {
    var arr = deviceStatusChart.w.globals.series.slice()
    arr.pop()
    return arr;
}

function randomize() {
    return deviceStatusChart.w.globals.series.map(function() {
        return Math.floor(Math.random() * (100 - 1 + 1)) + 1
    })
}

function reset() {
    return optionsDevice.series
}

document.querySelector("#randomize").addEventListener("click", function() {
    deviceStatusChart.updateSeries(randomize())
});

document.querySelector("#add").addEventListener("click", function() {
    deviceStatusChart.updateSeries(appendData())
});

document.querySelector("#remove").addEventListener("click", function() {
    deviceStatusChart.updateSeries(removeData())
});

document.querySelector("#reset").addEventListener("click", function() {
    deviceStatusChart.updateSeries(reset())
});



