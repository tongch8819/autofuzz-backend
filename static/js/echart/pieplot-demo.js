// init echarts with dark theme
var pieChart = echarts.init(document.getElementById('pieplot'), 'dark');
var option = {
    series: [
        {
            name: '访问来源',
            type: 'pie',    // 设置图表类型为饼图
            radius: '55%',  // 饼图的半径，外半径为可视区尺寸（容器高宽中较小一项）的 55% 长度。
            roseType: 'angle',  // coxcomb pie chart
            data: [          // 数据数组，name 为数据项名称，value 为数据项值
                { value: 235, name: '视频广告' },
                { value: 274, name: '联盟广告' },
                { value: 310, name: '邮件营销' },
                { value: 335, name: '直接访问' },
                { value: 400, name: '搜索引擎' }
            ],
            itemStyle: {
                normal: {
                    shadowBlur: 200,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};
pieChart.setOption(option);