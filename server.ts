import '@angular/localize/init';
import 'zone.js/dist/zone-node';
import { APP_BASE_HREF } from '@angular/common';
import { ngExpressEngine } from '@nguniversal/express-engine';
import { existsSync } from 'fs';
import { join } from 'path';
import { AppServerModule } from './src/main.server';
import express from 'express';
import cors from 'cors';
import request from 'request';
const port = process.env.PORT || 4000;

export function app(): express.Express {
	const server = express();
	server.use(express.json({limit: '50mb'}));
	server.use(express.urlencoded({limit: '50mb'}));
	server.use(cors({
		origin: 'http://localhost:4200',
		credentials: true,
	}));
	const distFolder = join(process.cwd(), 'dist/jibot3/browser');
	const indexHtml = existsSync(join(distFolder, 'index.original.html')) ? 'index.original.html' : 'index';
	server.engine('html', ngExpressEngine({
		bootstrap: AppServerModule,
	}));
	server.get('/gutenberg/**', (req, res) => {
		let gutenbergUrl = req.path.replace("/gutenberg/", "");
		request({ url: gutenbergUrl },
			(error, response, body) => {
				if (error || response.statusCode !== 200) {
					return res.status(500).json({ type: 'error', message: error.message });
				}
				res.send(body);
			}
		)
	});
	server.set('view engine', 'html');
	server.set('views', distFolder);
	server.get('*.*', express.static(distFolder, {
		maxAge: '1y'
	}));
	server.get('*', (req, res) => {
		res.render(indexHtml, { req, providers: [{ provide: APP_BASE_HREF, useValue: req.baseUrl }] });
	});
	return server;
}
function run(): void {
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