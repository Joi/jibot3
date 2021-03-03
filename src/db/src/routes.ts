import { BookController } from "./controller/BookController";
export const Routes = [{
    method: "get",
    route: "/books",
    controller: BookController,
    action: "all"
}, {
    method: "get",
    route: "/books/:id",
    controller: BookController,
    action: "one"
}, {
    method: "post",
    route: "/books",
    controller: BookController,
    action: "save"
}, {
    method: "delete",
    route: "/books/:id",
    controller: BookController,
    action: "remove"
}];