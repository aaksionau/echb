// Less configuration
const gulp = require("gulp");
const less = require("gulp-less");
const cleanCSS = require("gulp-clean-css");
const rename = require("gulp-rename");
const minify = require("gulp-minify");
const concat = require("gulp-concat");

gulp.task("make-map", () => {
  return gulp
    .src("./static/js/map/*.js")
    .pipe(concat("map.js"))
    .pipe(minify())
    .pipe(gulp.dest("js"));
});

gulp.task("make-css", () => {
  return gulp
    .src("./static/css/less/styles.less")
    .pipe(less())
    .pipe(gulp.dest("./css"))
    .pipe(cleanCSS({ compatibility: "ie8" }))
    .pipe(rename("styles.min.css"))
    .pipe(gulp.dest("./css"));
});

gulp.task("default", ["make-css", "make-map"], function() {
  gulp.watch("./css/less/*.less", ["make-css"]);
  gulp.watch("./js/map/*.js", ["make-map"]);
});
