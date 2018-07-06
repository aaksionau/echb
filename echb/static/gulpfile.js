// Less configuration
var gulp = require('gulp');
var less = require('gulp-less');

gulp.task('less', function() {
    gulp.src('./css/less/styles.less')
        .pipe(less())
        .pipe(gulp.dest('./css'));
});

gulp.task('default', ['less'], function() {
    gulp.watch('./css/less/*.less', ['less']);
});