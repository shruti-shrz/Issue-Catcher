const mongoose = require('mongoose');

const RepoSchema = new mongoose.Schema({
  name: {
    type: String,
    require: true
  },
  issues_url: {
    type: String,
    required: true
  },
  stargazers_count: {
    type: Number,
    default:0
  },
  forks_count:{
    type: Number,
    default:0
  },
  open_issues_count: {
    type: Number,
    default: 0
  },
  closed_issues_count: {
    type: Number,
    default: 0
  },
  score: {
    type: Number,
    default:0
  }
});

mongoose.model("Repo", RepoSchema);