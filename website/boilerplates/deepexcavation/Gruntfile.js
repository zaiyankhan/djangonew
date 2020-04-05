/*global module:false*/
module.exports = function (grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        favicons: {
            options: {
                trueColor: true,
                precomposed: true,
                appleTouchBackgroundColor: "#f5f5f5",
                coast: false,
                windowsTile: true,
                tileBlackWhite: false,
                androidHomescreen: true,
                tileColor: "#f5f5f5",
                html: 'templates/includes/favicons.html',
                HTMLPrefix: "{{ STATIC_URL }}ico/"
            },
            icons: {
                src: 'assets/logo_icon.png',
                dest: 'static/ico'
            }
        },
        postcss: {
            dev: {
                options: {
                    map: false,
                    processors: [
                        require('pixrem')(), // add fallbacks for rem units
                        require('autoprefixer')({browsers: 'last 2 versions'}), // add vendor prefixes
                    ]
                },
                src: ['../static/css/full/*.css',]
            },
            dist: {
                options: {
                    map: false,
                    processors: [
                        require('pixrem')(), // add fallbacks for rem units
                        require('autoprefixer')({browsers: 'last 2 versions'}), // add vendor prefixes
                        require('cssnano')({zindex: false}) // minify the result
                    ]
                },
                src: ['../static/css/*.css', '../static/jbrowse/genome.css']
            }
        },
        less: {
            development: {
                options: {
                    paths: ["less"]
                },
                files: {
                    "static/css/style.full.css": "less/style.less",
                }
            },
            production: {
                options: {
                    paths: ["less"],
                    compress: true,
                    cleancss: true
                },
                files: {
                    "static/css/style.css": "less/style.less",
                }
            }
        },
        concat: {
            options: {
                separator: ';'
            },
            dist: {
                src: [
                    'js/main.js'
                ],
                dest: 'static/js/main.full.js'
            },
        },
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
            },
            dist: {
                files: {
                    'static/js/main.js': ['<%= concat.dist.dest %>'],
                }
            }
        },
        jshint: {
            files: ['Gruntfile.js', 'js/**/*.js'],
            options: {
                // options here to override JSHint defaults
                globals: {
                    jQuery: true,
                    console: true,
                    module: true,
                    document: true
                }
            }
        },
        watch: {
            css: {
                files: "less/**/*.less",
                tasks: ["less", "postcss"]
            },
            js: {
                files: ['<%= jshint.files %>'],
                tasks: ['concat', 'uglify']
            }
        }
    });

    // These plugins provide necessary tasks.
    grunt.loadNpmTasks('grunt-favicons');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-postcss');
    // Default task.
    grunt.registerTask('build-favicons', ['favicons']);
    grunt.registerTask('default', ['less:development', 'postcss:dev', 'concat', 'uglify']);

    grunt.registerTask('production', ['less:production', 'postcss:dist', 'concat', 'uglify']);

};
