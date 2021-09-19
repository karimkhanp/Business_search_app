module.exports = {
  apps: [
    {
      exec_mode: 'cluster',
      name: 'testingFE4',
      cwd: '/home/ubuntu/Test-dir/Business_search_app',
      script: './FrontEnd/node_modules/nuxt/bin/nuxt.js',
      ref  : "origin/business_search_app10",
      repo: "https://github.com/karimkhanp/Business_search_app.git",
      port: 9000,
      instances: 'max',
      args: 'start'
    },

  ]
};
