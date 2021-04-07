import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { MaterialModule } from './modules/material.module';
import { NavComponent } from '@app/components/nav/nav.component';
import { HeaderComponent } from '@app/components/header/header.component';
import { FooterComponent } from '@app/components/footer/footer.component';
import { OptionsComponent } from '@pages/options/options.component';
import { BooksComponent, EditBookComponent } from '@pages/books';

@NgModule({
    bootstrap: [AppComponent],
	declarations: [
		AppComponent,
		NavComponent,
		HeaderComponent,
		FooterComponent,
		BooksComponent, EditBookComponent,
		OptionsComponent
	],
	exports: [
		MaterialModule,
	],
	imports: [
		BrowserModule.withServerTransition({ appId: 'jibot3' }),
		FormsModule,
        ReactiveFormsModule,
        NgbModule,
		HttpClientModule,
		AppRoutingModule,
		BrowserAnimationsModule,
		MaterialModule,
	],
	providers: [],

})
export class AppModule {}
