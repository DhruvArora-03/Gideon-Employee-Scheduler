import { Component } from "@angular/core";

@Component({
    selector: 'app-post-create',
    templateUrl: './post-create.component.html'
})
export class PostCreateComponent {
    enteredValue = '';
    postData = 'NO CONTENT YET';

    onAddPost() {
        this.postData = this.enteredValue;
    }
}