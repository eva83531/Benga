import React from 'react';
import ReactDOM from 'react-dom';
import DropzoneComponent from 'react-dropzone-component';
import Header from './header.jsx';
import Footer from './footer.jsx';
import Upload from './test.jsx';

// Render

class Main extends React.Component {

    constructor(props) {
        super(props);

        // For a full list of possible configurations,
        // please consult http://www.dropzonejs.com/#configuration
        this.djsConfig = {
            dictDefaultMessage:"Drop files or click to upload files",
            addRemoveLinks: true,
            acceptedFiles: ".fasta,.fa,.fna",
            autoProcessQueue: false,
            parallelUploads:200,
        };

        this.componentConfig = {
            iconFiletypes: ['.fasta','.fna','.fa'],
            showFiletypeIcon: true,
            postUrl: '/uploadHandler'
        };

        this.dropzone = null;
    }

    handleFileAdded(file) {
        console.log(file);
    }

    handlePost() {
        this.dropzone.processQueue();
    }

    reload(){
        window.location.reload();
    }

    
    render() {
        const config = this.componentConfig;
        const djsConfig = this.djsConfig;

        // For a list of all possible events (there are many), see README.md!
        const eventHandlers = {
            init: dz => this.dropzone = dz,
            addedfile: this.handleFileAdded.bind(this)
        }

        return (
            <div>
                <div>
                <Header />
                </div>
                <br />
                <br />
                <DropzoneComponent config={config} eventHandlers={eventHandlers} djsConfig={djsConfig} />
                <br />
                <button onClick={this.handlePost.bind(this)}> Upload </button> &nbsp;&nbsp;&nbsp;&nbsp;
                <button onClick={this.reload}> Reset </button>
                <br />
                <br />
                <div>
                <Footer />
                </div>

            </div>
        );
    }
}

ReactDOM.render(<Main /> ,document.getElementById('host'));
