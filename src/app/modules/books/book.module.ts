import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BookService } from  './book.service';
import { AddBookComponent, BooksComponent, EditBookComponent } from './components';
import { MaterialModule } from '../material/material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
@NgModule({
	declarations: [
		BooksComponent,
        AddBookComponent,
        EditBookComponent
	],
	exports: [
        MaterialModule,
        FormsModule,
        ReactiveFormsModule,
        RouterModule
    ],
	imports: [
		CommonModule,
		MaterialModule,
        RouterModule,
        ReactiveFormsModule
	],
	providers: [
		BookService
	]
})
export class BookModule { }
