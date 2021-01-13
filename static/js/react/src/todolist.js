'use strict';

const e = React.createElement;

class LikeButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = { liked: false };
    }

    render() {
        if (this.state.liked) {
            return 'You liked this.';
        }

        return e(
            'button',
            { onClick: () => this.setState({ liked: true }) },
            'Like'
        );
    }
}

// const domContainer = document.querySelector('#root');
const domContainer = document.getElementById('root');
// ReactDOM.render(e(LikeButton), domContainer);
ReactDOM.render(<h2>Hello World</h2>, document.getElementById("root"));