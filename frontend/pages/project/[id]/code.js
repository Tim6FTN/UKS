import Container from "../../../components/util/container";
import Navbar from "../../../components/util/navbar";
import BranchList from "../../../components/branch/list";
import { useEffect, useState } from "react";
import CommitList from "../../../components/commit/list";
import { useRouter } from "next/router";
import CodeService from "../../../services/codeService";
import withAuth from "../../../components/util/withAuth";

const Code = () => {
  const [branches, setBranches] = useState([]);
  const [commits, setCommits] = useState([]);

  const [active, setActive] = useState("");
  const handleSelect = (event) => {
    let value = event.target.value;
    if (value !== "") {
      const selectedBranch = branches.find(
        (branch) => branch.id == event.target.value
      );
      value = selectedBranch.id;
    }
    setActive(value);
  };
  useEffect(() => {
    if (active) {
      getCommits(active);
    }
  }, [active]);

  const getBranches = async (id) => {
    const response = await CodeService.getBranches(id);
    setBranches(response.data);
  };
  const addBranch = async (branch) => {
    await CodeService.createBranch(router.query.id, branch);
    getBranches(router.query.id);
  };

  const getCommits = async (id) => {
    const response = await CodeService.getCommits(id);
    setCommits(response.data);
  };
  const addCommit = async (commit) => {
    await CodeService.createCommit(active, commit);
    getCommits(active);
  };

  const router = useRouter();
  useEffect(() => {
    if (router.query.id) {
      getBranches(router.query.id);
    }
  }, [router.query.id]);

  return (
    <div>
      <Navbar />
      <Container>
        <BranchList
          branches={branches}
          active={active}
          handleChange={handleSelect}
          handleAdd={addBranch}
        />

        <CommitList commits={commits} handleAdd={addCommit} />
      </Container>
    </div>
  );
};

export default withAuth(Code);
