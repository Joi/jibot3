import "reflect-metadata";
import {createConnection} from "typeorm";
import * as express from "express";
import * as bodyParser from "body-parser";
import * as cors from 'cors';
import { Request, Response } from "express";
import { Routes } from "./routes";
export const database = createConnection().then(async connection => {
    const app = express();
    app.use(cors());
	app.use(bodyParser.urlencoded({ extended: true }));
	app.use(express.json({limit: '500mb'}));
	app.use(express.urlencoded({limit: '500mb'}));
	Routes.forEach(route => {
		(app as any)[route.method](route.route, (req: Request, res: Response, next: any) => {
            const result = (new (route.controller as any)())[route.action](req, res, next);
            if (result instanceof Promise) {
                result.then(r => r !== null && r !== undefined ? res.send(r) : undefined);
            } else if (result !== null && result !== undefined) {
                res.json(result);
            }
        });
    });
    app.listen(3000);
    console.log("Jibot Database has started on port 3000. Open http://localhost:3000/books to see results");
    return app;
}).catch(error => console.log(error));
