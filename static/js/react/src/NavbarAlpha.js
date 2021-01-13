// import React from 'react'
// import ReactDOM from 'react-dom'
// import NavbarColumn from './NavbarColumn.js'


class NavbarAlpha extends React.Component {
    constructor() {
        super();
        this.state = {
            id: 1,
        }
    }

    render() {
        return (
            <nav className="col-md-2 d-none d-md-block bg-light sidebar">
                <div className="sidebar-sticky">
                    <NavbarColumn />
                </div>
            </nav>
        )
    }
}

ReactDOM.render(<NavbarAlpha />, document.getElementById('NavbarAlpha'))
// ReactDOM.render(<h1>Hello world</h1>, document.getElementById('NavbarAlpha'))