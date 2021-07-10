module.exports = {
  apps: [
    {
      exec_mode: 'cluster',
      name: 'testingFE1',
      cwd: '/home/ubuntu/TestDir/FrontEnd',
      script: './node_modules/nuxt/bin/nuxt.js',
      port: 3030,
      instances: 'max',
      args: 'start'
    },

  ]
};
