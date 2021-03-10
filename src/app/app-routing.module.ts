import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BooksComponent } from '@pages/books/books.component';
import { OptionsComponent } from '@pages/options/options.component';
export const routes: Routes = [
	{ path: '', pathMatch: 'full', redirectTo: 'books' },
    { path: 'books', component: BooksComponent },
	{ path: 'options', component: OptionsComponent }
];
@NgModule({
	declarations: [],
	imports: [RouterModule.forRoot(routes)],
	exports: [RouterModule]
})
export class AppRoutingModule { }