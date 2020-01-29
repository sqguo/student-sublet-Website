'use strict';

const e = React.createElement;

function SubletPost(props) {
    return (
        <li className="list-group-item list-group-item-action" onClick={props.onClick}>
            <h2>{props.title}</h2> {props.description}
        </li>
    );
}

class SubletList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            sublets: Array(0),
        };
    }

    handleClick(i) {
        console.log("clicked", i);
    }

    renderSubletPost(i) {
        return (
            <SubletPost
                title={this.state.sublets[i]['title']}
                description={this.state.sublets[i]['description']}
                onClick={() => this.handleClick(i)}
            />
        );
    }
    createSubletRows() {
        let list = [];
        for (let i = 0; i < this.state.sublets.length; i++) {
            list.push(this.renderSubletPost(i));
        }
        return list;
    }
    refresh() {
        $.ajax({
            type: 'GET',
            url: '/api/v0/sublet',
            success: function (data) {
                this.setState({
                    sublets: data,
                });
            }.bind(this),
            contentType: "application/json",
        });
    }

    render() {
        return (
            <div>
                <AddRefreshButton onClick={() => this.refresh()} />
                <div className="list-group">
                    {this.createSubletRows()}
                </div>
            </div>
        );
    }
}

class AddSubletButton extends React.Component {
    constructor(props) {
        super(props);
    }
    // replace below !!
    createSublet() {
        $.ajax({
            type: 'POST',
            url: '/api/v0/sublet',
            data: JSON.stringify({
                'latitude': 11,
                'longitude': 11,
                'title': "new test 4 month posting",
                'description': "new sublet test post description"
            }),
            success: function (data) {
                console.log(data);
            },
            contentType: "application/json",
            dataType: 'json'
        });
    }

    render() {
        return e(
            'button',
            { onClick: () => this.createSublet() },
            '+'
        );
    }
}

function AddRefreshButton(props) {
    return (
        <button onClick={props.onClick}>
            refresh
        </button>
    );
}

const domContainer = document.querySelector('#adsublet_button_container');
const domContainer2 = document.querySelector('#sublet_list_container');
ReactDOM.render(e(AddSubletButton), domContainer);
ReactDOM.render(e(SubletList), domContainer2);