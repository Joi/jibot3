import {  NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BooksComponent, EditBookComponent } from './components';
import { MaterialModule } from '@app/modules/material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { BookService, BookServiceFactory } from './book.service';
import { HttpClient } from '@angular/common/http';
@NgModule({
	declarations: [
		BooksComponent,
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
		{
			provide: BookService,
			useFactory: BookServiceFactory,
			deps: [HttpClient]
		}
	]
})
export class BookModule { }
