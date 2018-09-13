// Less configuration
var gulp = require('gulp');
var less = require('gulp-less');
var cleanCSS = require('gulp-clean-css');
let rename = require('gulp-rename');

gulp.task('make-css', () => {
    return gulp.src('./css/less/styles.less')
        .pipe(less())
        .pipe(gulp.dest('./css'))
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(rename('styles.min.css'))
        .pipe(gulp.dest('./css'));
});

gulp.task('default', ['make-css'], function() {
    gulp.watch('./css/less/*.less', ['make-css']);
});