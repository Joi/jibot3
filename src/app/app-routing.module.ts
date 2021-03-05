import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
// import { EditBookComponent } from '@modules/books/components/edit-book/edit-book.component';
import { BooksComponent } from '@modules/books/components/books.component';
export const routes: Routes = [
	{ path: '', pathMatch: 'full', redirectTo: 'books' },
    { path: 'books', component: BooksComponent },
];
@NgModule({
	declarations: [],
	imports: [RouterModule.forRoot(routes)],
	exports: [RouterModule]
})
export class AppRoutingModule { }