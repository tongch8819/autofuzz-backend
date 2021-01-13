// import React from 'react'
// import ReactDOM from 'react-dom'

// import NavbarColumnItem from './NavbarColumnItem.js'

class NavbarColumn extends React.Component {
    constructor() {
        super();
        this.state = {

        }
    }

    render() {
        return (
            <ul className="nav flex-column">
                <NavbarColumnItem content='主页' iconName='home' url='index'/>
                <NavbarColumnItem content='压缩包上传' iconName='file-plus' url='uploadCompress'/>
                <NavbarColumnItem content='Git URL上传' iconName='file-plus' url='uploadGitURL'/>
                <NavbarColumnItem content='测试用例上传' iconName='file' url='uploadInputSeeds'/>
                <NavbarColumnItem content='插桩编译' iconName='settings' url='compile'/>
                <NavbarColumnItem content='模糊测试运行' iconName='settings' url='runtime'/>
                <NavbarColumnItem content='状态监控' iconName='settings' url='status'/>
                <NavbarColumnItem content='生成分析报告' iconName='settings' url='PDFReport'/>
            </ul>
        )
    }
}

// export default NavbarColumn