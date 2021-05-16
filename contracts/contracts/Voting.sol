pragma solidity 0.4.24;

contract Election  {
    struct Candidate {
        uint id;
        string name;
        string party;
        uint voteCount;
    }
    // bool goingon = true;
    mapping(address => bool) public voters;
    mapping(uint => Candidate) public candidates;
    uint public candidatesCount;

    // event votedEvent (
    //     uint indexed _candidateId
    // ); 

    constructor () public {
        addCandidate("Candidate 1", "bjp");
        addCandidate("Candidate 2", "inc");
        addCandidate("Candidate 3", "aitc");
        addCandidate("Candidate 4", "aap");
        addCandidate("Candidate 5", "cpi");
        addCandidate("Candidate 6", "ss");
        addCandidate("None of above", "nota");
    }

    function addCandidate (string memory _name, string memory _party) private {
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, _party, 0);
    }

    // function end () public {
    //     goingon = false;
    // }

    function vote (uint _candidateId) public {
        // require(!voters[msg.sender],"Already voted");

        require(_candidateId > 0 && _candidateId <= candidatesCount,"Invalid candidate");

        // require(goingon,"Election ended");

        voters[msg.sender] = true;

        candidates[_candidateId].voteCount ++;

        // emit votedEvent(_candidateId);
    }
}