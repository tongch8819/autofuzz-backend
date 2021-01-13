// import React from 'react'
// import ReactDOM from 'react-dom'


class NavbarColumnItem extends React.Component {
    constructor() {
        super()
        this.state = {

        }
    }

    render() {
        return (
            <li className="nav-item">
                <a className="nav-link" href={this.props.url}>
                    <span data-feather={this.props.iconName}></span>
                    {this.props.content}
                </a>
            </li>
        )
    }
}

// export default NavbarColumnItem