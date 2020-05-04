'use strict';

const e = React.createElement;

function SubletPost(props) {
    return (
        <li className="list-group-item list-group-item-action" onClick={props.handleClick}>
            <h2>{props.title}</h2> {props.description}
        </li>
    );
}

function RefreshSubletListButton(props) {
    return <button onClick={props.handleClick}>refresh</button>
}

function AddSubletPostButton(props) {
    return <button onClick={props.handleClick}>+</button>
}

class AddsubletPostInputForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            postTitle: "",
            postDescription: "",
        }
        this.handleAddPostButtonClick = this.handleAddPostButtonClick.bind(this); 
        this.handleDescriptionChange = this.handleDescriptionChange.bind(this); 
        this.handleTitleChange = this.handleTitleChange.bind(this); 
    }

    handleAddPostButtonClick() {
        $.ajax({
            type: 'POST',
            url: '/api/v0/sublet',
            data: JSON.stringify({
                //testing position
                'latitude': 11,
                'longitude': 11,
                'title': this.state.title,
                'description': this.state.description
            }),
            success: function (data) {
                //testing
                console.log("post added to database")
                console.log(data);
            }.bind(this),
            contentType: "application/json",
            dataType: 'json'
        });
    }

    handleTitleChange(event) {
        this.setState({title: event.target.value}); 
    }

    handleDescriptionChange(event) {
        this.setState({description: event.target.value}); 
    }

    render() {
        return (
            <div>
                <label>
                    Title:<br/>
                    <input type="text" value={this.state.title} onChange={this.handleTitleChange} />
                    <br/>
                    Description:<br/>
                    <textarea value={this.state.description} onChange={this.handleDescriptionChange} />
                    <br/>
                </label>
                <AddSubletPostButton handleClick={this.handleAddPostButtonClick}/>
            </div>
        );
    }
}

class SubletPostList extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div className="list-group">
                {this.props.subletData.map((sublet, index) =>
                    <SubletPost
                        key={sublet['id'].toString()}
                        title={sublet['title']}
                        description={sublet['description']}
                        handleClick={() => this.props.handleClick(index)}
                    />
                )}
            </div>
        );
    }
}

class SubletListContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            subletData: Array(0),
        };
        this.handleRefreshButtonClick = this.handleRefreshButtonClick.bind(this);
        this.handleListItemClick = this.handleListItemClick.bind(this);
    }

    handleRefreshButtonClick() {
        $.ajax({
            type: 'GET',
            url: '/api/v0/sublet',
            success: function (data) {
                this.setState({
                    subletData: data,
                });
                //testing
                console.log("refreshed listing");
            }.bind(this),
            contentType: "application/json",
        });
    }

    handleListItemClick(index) {
        //testing
        console.log("clicked", index);
        console.log(this.state.subletData[index]);
    }
    render() {
        return (
            <div class="subletListContainer">
                <RefreshSubletListButton handleClick={this.handleRefreshButtonClick} />
                <SubletPostList subletData={this.state.subletData} handleClick={this.handleListItemClick} />
            </div>
        );
    }
}

function SubletMainInterface(props) {
    return (
        <div>
            <SubletListContainer/>
            <AddsubletPostInputForm/>
        </div>
    )
}

//should change to single node
//always capital case for react component, event camelcase
//never modify own props
//state =  in constructor, else use set state
//single source of truth
const root = document.querySelector('#root');
ReactDOM.render(e(SubletMainInterface), root);