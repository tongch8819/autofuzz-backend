
let xhr = new XMLHttpRequest();
xhr.open('GET', '/autofuzz/api/disk', true);
xhr.responseType = 'text';
// xhr.onload = () => alert(`Loaded: ${xhr.status} ${xhr.response}`);
xhr.onload = function () {
    var raw_data = xhr.response;
    var obj = JSON.parse(raw_data);

    // construct
    plot_data = []
    var i;
    var total_size = 0;
    // obj.projects is an array
    for (i = 0; i < obj.projects.length; i++) {
        var ele = obj.projects[i];
        plot_data.push({ value: parseInt(ele.size), name: ele.name });
        total_size += parseInt(ele.size);

    }

    // init echarts with dark theme
    var pieChart = echarts.init(document.getElementById('pieplot'), 'dark');
    var option = {
        dataZoom: [
            {   // 这个dataZoom组件，默认控制x轴。
                type: 'slider', // 这个 dataZoom 组件是 slider 型 dataZoom 组件
                start: 10,      // 左边在 10% 的位置。
                end: 60         // 右边在 60% 的位置。
            }
        ],
        series: [
            {
                name: '访问来源',
                type: 'pie',    // 设置图表类型为饼图
                radius: '55%',  // 饼图的半径，外半径为可视区尺寸（容器高宽中较小一项）的 55% 长度。
                data: plot_data,
                itemStyle: {
                    normal: {
                        shadowBlur: 200,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    console.log(option.roseType);
    pieChart.setOption(option);


    // render total size
    console.log(total_size);
    document.getElementById('total-disk-usage').innerHTML = '<p>Total size: ' + String(total_size) + 'M;</p>';
}
xhr.send();


// function loadXMLDoc()
// {
	// var xmlhttp;
	// if (window.XMLHttpRequest)
	// {
		//  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
		// xmlhttp=new XMLHttpRequest();
	// }
	// else
	// {
		// IE6, IE5 浏览器执行代码
		// xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	// }
	// xmlhttp.onreadystatechange=function()
	// {
		// if (xmlhttp.readyState==4 && xmlhttp.status==200)
		// {
            // console.log(xmlhttp.responseXML);
            // return xmlhttp.responseXML;
		// }
	// }
	// xmlhttp.open("GET","/autofuzz/api/disk",true);
	// xmlhttp.send();
// }


// var data;
// $.getJSON('http://127.0.0.1/autofuzz/api/disk', function(data) {});
// console.log(data);
