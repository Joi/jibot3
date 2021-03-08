import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Book } from '../../book';
import { BookService } from '../../book.service';

@Component({
  selector: 'app-edit-book',
  templateUrl: './edit-book.component.html',
  styleUrls: ['./edit-book.component.scss']
})
export class EditBookComponent implements OnInit {
	@Input() book: Book;
	@Output() onChange = new EventEmitter();
	@Output() onDelete = new EventEmitter();

	public action: string = "edit";
    public formGroup: FormGroup;
	constructor(
		private formBuilder: FormBuilder,
		private bookService: BookService
	) { }
	ngOnInit(): void {
		if (!this.book) {
			this.book = new Book();
			this.action = "add";
		}
		this.formGroup = this.formBuilder.group(this.book);
	}
	public update = (book:Book) => {
		// this.bookService.update(book).subscribe(
        //     (books) => {
		// 		this.book = book;
		// 		this.onChange.emit(books);
		// 	},
        //     console.error
        // );
    }
	public delete = (book:Book) => {
        // this.bookService.delete(book).subscribe(
        //     (r) => {
        //         console.log(r);
        //         console.log("DELETED");
        //     },
        //     console.error
        // );
    }
}
