var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

// import React from 'react'
// import ReactDOM from 'react-dom'

// import NavbarColumnItem from './NavbarColumnItem.js'

var NavbarColumn = function (_React$Component) {
    _inherits(NavbarColumn, _React$Component);

    function NavbarColumn() {
        _classCallCheck(this, NavbarColumn);

        var _this = _possibleConstructorReturn(this, (NavbarColumn.__proto__ || Object.getPrototypeOf(NavbarColumn)).call(this));

        _this.state = {};
        return _this;
    }

    _createClass(NavbarColumn, [{
        key: 'render',
        value: function render() {
            return React.createElement(
                'ul',
                { className: 'nav flex-column' },
                React.createElement(NavbarColumnItem, { content: '\u4E3B\u9875', iconName: 'home', url: 'index' }),
                React.createElement(NavbarColumnItem, { content: '\u538B\u7F29\u5305\u4E0A\u4F20', iconName: 'file-plus', url: 'uploadCompress' }),
                React.createElement(NavbarColumnItem, { content: 'Git URL\u4E0A\u4F20', iconName: 'file-plus', url: 'uploadGitURL' }),
                React.createElement(NavbarColumnItem, { content: '\u6D4B\u8BD5\u7528\u4F8B\u4E0A\u4F20', iconName: 'file', url: 'uploadInputSeeds' }),
                React.createElement(NavbarColumnItem, { content: '\u63D2\u6869\u7F16\u8BD1', iconName: 'settings', url: 'compile' }),
                React.createElement(NavbarColumnItem, { content: '\u6A21\u7CCA\u6D4B\u8BD5\u8FD0\u884C', iconName: 'settings', url: 'runtime' }),
                React.createElement(NavbarColumnItem, { content: '\u72B6\u6001\u76D1\u63A7', iconName: 'settings', url: 'status' }),
                React.createElement(NavbarColumnItem, { content: '\u751F\u6210\u5206\u6790\u62A5\u544A', iconName: 'settings', url: 'PDFReport' })
            );
        }
    }]);

    return NavbarColumn;
}(React.Component);

// export default NavbarColumn