import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { BookModule } from './modules/books/book.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './modules/material.module';
import { NavComponent } from './components/nav/nav.component';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { OptionsModule } from './modules/options/options.module';

@NgModule({
    bootstrap: [AppComponent],
	declarations: [
		AppComponent,
		NavComponent,
		HeaderComponent,
		FooterComponent,
	],
	exports: [MaterialModule],
	imports: [
		BrowserModule.withServerTransition({ appId: 'jibot3' }),
        NgbModule,
		HttpClientModule,
		AppRoutingModule,
		BrowserAnimationsModule,
		MaterialModule,
		BookModule,
		OptionsModule
	],
	providers: [],
	
})
export class AppModule {}
