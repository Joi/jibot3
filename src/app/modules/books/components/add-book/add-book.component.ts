import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl } from '@angular/forms';
import { Book } from '../../book';
@Component({
  selector: 'app-add-book',
  templateUrl: './add-book.component.html',
  styleUrls: ['./add-book.component.scss']
})
export class AddBookComponent implements OnInit {
    public book: Book = new Book();
    public form: FormGroup;
    constructor(
        private formBuilder: FormBuilder 
    ) { 
        this.form = this.formBuilder.group(this.book);
    }
    ngOnInit(): void {
        //console.log(this.form);
    }
}
