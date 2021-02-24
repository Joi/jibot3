import 'zone.js/dist/zone-node';
import { APP_BASE_HREF } from '@angular/common';
import { ngExpressEngine } from '@nguniversal/express-engine';
import * as express from 'express';
import { existsSync } from 'fs';
import { join } from 'path';
import { AppServerModule } from './src/main.server';


//const sqlite3 = require("sqlite3").verbose();

//import { open } from 'sqlite';
// (async () => {
//     const db = await open({
// 		filename: '/tmp/database.db',
// 		driver: sqlite3.Database
//     });
// 	console.log(db);
// })();

// The Express app is exported so that it can be used by serverless Functions.
export function app(): express.Express {
	// const db_file = join(process.cwd(), "data", "jibot.db");
	// const db = new sqlite3.Database(db_file, err => {
	// 	if (err) {
	// 		return console.error(err.message);
	// 	}
	// 	console.log("Successful connection to the database 'apptest.db'");
	// });
	//
	// const db = new sqlite3.Database(db_file, err => {
	// 	if (err) {
	// 	  return console.error(err.message);
	// 	}
	// 	console.log("Successful connection to the database 'apptest.db'");
	//   });
	const server = express();
	const distFolder = join(process.cwd(), 'dist/jibot3/browser');
	const indexHtml = existsSync(join(distFolder, 'index.original.html')) ? 'index.original.html' : 'index';

	// Our Universal express-engine (found @ https://github.com/angular/universal/tree/master/modules/express-engine)
	server.engine('html', ngExpressEngine({
		bootstrap: AppServerModule,
	}));

	server.set('view engine', 'html');
	server.set('views', distFolder);

	// Example Express Rest API endpoints
	// server.get('/api/**', (req, res) => { });
	// Serve static files from /browser
	server.get('*.*', express.static(distFolder, {
		maxAge: '1y'
	}));

	// All regular routes use the Universal engine
	server.get('*', (req, res) => {
		res.render(indexHtml, { req, providers: [{ provide: APP_BASE_HREF, useValue: req.baseUrl }] });
	});

	return server;
}

function run(): void {
  const port = process.env.PORT || 4000;

  // Start up the Node server
  const server = app();
  server.listen(port, () => {
    console.log(`Node Express server listening on http://localhost:${port}`);
  });
}

// Webpack will replace 'require' with '__webpack_require__'
// '__non_webpack_require__' is a proxy to Node 'require'
// The below code is to ensure that the server is run only when not requiring the bundle.
declare const __non_webpack_require__: NodeRequire;
const mainModule = __non_webpack_require__.main;
const moduleFilename = mainModule && mainModule.filename || '';
if (moduleFilename === __filename || moduleFilename.includes('iisnode')) {
  run();
}

export * from './src/main.server';
