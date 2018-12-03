// Less configuration
const gulp = require("gulp"),
  browserSync = require("browser-sync").create(),
  sass = require("gulp-sass"),
  cleanCSS = require("gulp-clean-css"),
  rename = require("gulp-rename"),
  minify = require("gulp-minify"),
  minifyCss = require('gulp-minify-css'),
  concat = require("gulp-concat"),
  autoprefixer = require('gulp-autoprefixer');

const exec = require('child_process').exec;

const pathToStatic = './echb/static/'

sass.compiler = require("node-sass");

gulp.task("server", function() {});

gulp.task("make-map", () => {
  return gulp
    .src("./echb/static/js/map/*.js")
    .pipe(concat("map.js"))
    .pipe(minify())
    .pipe(gulp.dest("./echb/static/js"));
});

gulp.task("make-css", () => {
  return gulp
    .src("./echb/static/css/style.sass")
    .pipe(sass().on("error", sass.logError))
    .pipe(autoprefixer('last 2 versions'))
    .pipe(minifyCss())
    .pipe(rename("style.min.css"))
    .pipe(gulp.dest("./echb/static/css"));
});

gulp.task('runserver', function() {
  var proc = exec('fab runserver')
})

gulp.task('browserSync', ['runserver'], function() {
  browserSync.init({
    notify: false,
    port: 8000,
    proxy: 'localhost:8000'
  })
});

gulp.task("default", ['make-css', 'make-map', 'browserSync'], function() {
  gulp.watch("./echb/static/css/**/**/*.sass", ["make-css"]);
  gulp.watch("./echb/static/css/style.min.css").on('change', browserSync.reload);
  gulp.watch("./echb/static/js/map/*.js", ["make-map"]);
});
