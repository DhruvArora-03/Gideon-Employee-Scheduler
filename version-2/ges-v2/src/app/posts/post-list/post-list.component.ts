import { Component, Input } from "@angular/core";

@Component({
    selector: 'app-post-list',
    templateUrl: './post-list.component.html',
    styleUrls: ['./post-list.component.css']
})
export class PostListComponent {
    @Input() posts : {title: string; content: string}[] = [];

    onPostAdded(post: { title: string; content: string; }) {
        this.posts.push(post);
    }
}