module.exports = {
  apps: [
    {
      exec_mode: 'cluster',
      name: 'testingFE1',
      cwd: '/home/ubuntu/Test-dir/Business_search_app/FrontEnd',
      script: './FrontEnd/node_modules/nuxt/bin/nuxt.js',
      ref  : "origin/business_search_app1",
      repo: "https://github.com/karimkhanp/Business_search_app.git",
      port: 2000,
      instances: 'max',
      args: 'start'
    },

  ]
};
