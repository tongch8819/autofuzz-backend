var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

// import React from 'react'
// import ReactDOM from 'react-dom'
// import NavbarColumn from './NavbarColumn.js'


var NavbarAlpha = function (_React$Component) {
    _inherits(NavbarAlpha, _React$Component);

    function NavbarAlpha() {
        _classCallCheck(this, NavbarAlpha);

        var _this = _possibleConstructorReturn(this, (NavbarAlpha.__proto__ || Object.getPrototypeOf(NavbarAlpha)).call(this));

        _this.state = {
            id: 1
        };
        return _this;
    }

    _createClass(NavbarAlpha, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "nav",
                { className: "col-md-2 d-none d-md-block bg-light sidebar" },
                React.createElement(
                    "div",
                    { className: "sidebar-sticky" },
                    React.createElement(NavbarColumn, null)
                )
            );
        }
    }]);

    return NavbarAlpha;
}(React.Component);

ReactDOM.render(React.createElement(NavbarAlpha, null), document.getElementById('NavbarAlpha'));
// ReactDOM.render(<h1>Hello world</h1>, document.getElementById('NavbarAlpha'))