module.exports = {
  apps: [
    {
      exec_mode: 'cluster',
      name: 'testingFE4',
      cwd: '/home/ubuntu/TestingFE4/Business_search_app',
      script: './FrontEnd/node_modules/nuxt/bin/nuxt.js',
      ref  : "origin/development",
      repo: "https://github.com/karimkhanp/Business_search_app.git",
      port: 9000,
      instances: 'max',
      args: 'start'
    },

  ]
};
